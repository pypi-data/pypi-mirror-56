import os
import importlib
import sys
import logging
import argparse
import time
import traceback
import cravat.constants as constants
from cravat.inout import CravatWriter
from cravat.exceptions import LiftoverFailure, InvalidData, BadFormatError, ExpectedException
import cravat.admin_util as au
from pyliftover import LiftOver
import copy
import cravat.cravat_util as cu
from cravat.util import detect_encoding
import json

class VTracker:
    """ This helper class is used to identify the unique variants from the input 
        so the crv file will not contain multiple copies of the same variant.
    """
    def __init__(self):
        self.var_by_chrom = {}
        self.current_UID = 1
    
    #Add a variant - Returns true if the variant is a new unique variant, false
    #if it is a duplicate.  Also returns the UID.
    def addVar(self, chrom, pos, ref, alt):
        change = ref+":"+alt
        if chrom not in self.var_by_chrom:
            self.var_by_chrom[chrom] = {}
        
        chr_dict = self.var_by_chrom[chrom]
        if pos not in chr_dict:
            #we have not seen this position before, add the position and change
            chr_dict[pos] = {}
            chr_dict[pos][change] = self.current_UID
            self.current_UID += 1
            return True, chr_dict[pos][change]
        else:
            variants = chr_dict[pos]
            if change not in variants:
                #we have the position but not this base change, add it.
                chr_dict[pos][change] = self.current_UID
                self.current_UID = self.current_UID + 1
                return True, chr_dict[pos][change]
            else:
                #this variant has been seen before.
                return False, chr_dict[pos][change] 

class MasterCravatConverter(object):
    """ Convert a file of ambiguous format to .crv format.
        
        Reads in CravatConverter classes in the same directory, selects the
        correct converter, and writes a crv file.
    """
    ALREADYCRV = 2
    def __init__(self, args=None, status_writer=None):
        args = args if args else sys.argv
        self.status_writer = status_writer
        # self.input_path = None
        # self.f = None
        self.input_paths = []
        self.input_files = []
        self.input_format = None
        self.logger = None
        self.crv_writer = None
        self.crs_writer = None
        self.crm_writer = None
        self.crl_writer = None
        self.primary_converter = None
        self.converters = {}
        self.possible_formats = []
        self.ready_to_convert = False
        self.cmd_args = None
        self.output_dir = None
        self.output_base_fname = None
        self.chromdict = {'chrx': 'chrX', 'chry': 'chrY', 'chrMT': 'chrM', 'chrMt': 'chrM', 'chr23': 'chrX', 'chr24': 'chrY'}
        self.vtracker = VTracker();
        self._parse_cmd_args(args)
        self._setup_logger()

    def _parse_cmd_args(self, args):
        """ Parse the arguments in sys.argv """
        parser = argparse.ArgumentParser()
        parser.add_argument('path',
                            help='Path to this converter\'s python module')
        parser.add_argument('inputs',
                            nargs='+',
                            help='Files to be converted to .crv')
        parser.add_argument('-f',
                            dest='format',
                            help='Specify an input format')
        parser.add_argument('-n', '--name',
                            dest='name',
                            help='Name of job. Default is input file name.')
        parser.add_argument('-d', '--output-dir',
                            dest='output_dir',
                            help='Output directory. '\
                                 +'Default is input file directory.')
        parser.add_argument('-l','--liftover',
                            dest='liftover',
                            choices=['hg38']+list(constants.liftover_chain_paths.keys()),
                            default='hg38',
                            help='Input gene assembly. Will be lifted over to hg38')
        parser.add_argument('--confs',
            dest='confs',
            default='{}',
            help='Configuration string')
        parsed_args = parser.parse_args(args)
        self.input_paths = [os.path.abspath(x) for x in parsed_args.inputs]
        self.input_path_dict = {}
        self.input_path_dict2 = {}
        for i in range(len(self.input_paths)):
            self.input_path_dict[i] = self.input_paths[i]
            self.input_path_dict2[self.input_paths[i]] = i
        if parsed_args.format:
            self.input_format = parsed_args.format
        self.input_dir = os.path.dirname(self.input_paths[0])
        if parsed_args.output_dir:
            self.output_dir = parsed_args.output_dir
        else:
            self.output_dir = self.input_dir
        if not(os.path.exists(self.output_dir)):
            os.makedirs(self.output_dir)
        if parsed_args.name:
            self.output_base_fname = parsed_args.name
        else:
            self.output_base_fname = os.path.basename(self.input_paths[0])
        self.input_assembly = parsed_args.liftover
        self.do_liftover = self.input_assembly != 'hg38'
        if self.do_liftover:
            self.lifter = LiftOver(constants.liftover_chain_paths[self.input_assembly])
        else:
            self.lifter = None
        self.status_fpath = os.path.join(self.output_dir, self.output_base_fname + '.status.json')
        self.confs = None
        if parsed_args.confs is not None:
            confs = parsed_args.confs.lstrip('\'').rstrip('\'').replace("'", '"')
            self.confs = json.loads(confs)

    def setup (self):
        """ Do necesarry pre-run tasks """
        if self.ready_to_convert: return
        # Open file handle to input path
        for input_path in self.input_paths:
            encoding = detect_encoding(input_path)
            self.input_files.append(open(input_path, encoding=encoding))
        # Read in the available converters
        self._initialize_converters()
        # Select the converter that matches the input format
        self._select_primary_converter()
        
        # A correct .crv file is not processed.
        #todo handle this for multiple inputs. have to convert them so they can be merged 
        # if self.input_format == 'crv' and \
        #     self.input_paths[0].split('.')[-1] == 'crv':
        #     self.logger.info('Input file is already a crv file. Exiting converter.')
        #     exit(0)
        
        # Open the output files
        self._open_output_files()
        self.ready_to_convert = True

    def _setup_logger(self):
        """ Open a log file and set up log handler """
        self.logger = logging.getLogger('cravat.converter')
        self.logger.info('started: %s' %time.asctime())
        self.logger.info('input files: %s' %', '.join(self.input_paths))
        if self.do_liftover:
            self.logger.info('liftover from %s' %self.input_assembly)
        self.error_logger = logging.getLogger('error.converter')
        self.unique_excs = []

    def _initialize_converters(self):
        """ Reads in available converters.
            
            Loads any python files in same directory that start with _ as
            python modules. Initializes the CravatConverter class from that
            module and places them in a dict keyed by their input format
        """
        for module_info in au.get_local_module_infos_of_type('converter').values():
            # path based import from https://docs.python.org/3/library/importlib.html#importing-a-source-file-directly
            spec = importlib.util.spec_from_file_location(module_info.name,
                                                          module_info.script_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            converter = module.CravatConverter()
            if converter.format_name not in self.converters:
                self.converters[converter.format_name] = converter
            else:
                err_msg = 'Cannot load two converters for format %s' \
                    %converter.format_name
                raise ExpectedException(err_msg)
        self.possible_formats = list(self.converters.keys())

    def _select_primary_converter(self):
        """ Choose the converter which matches the input format.
            
            If a input format was not specified in the cmd args, uses the 
            check_format() method of the CravatConverters to identify a
            converter which can parse the input file.
        """
        if self.input_format is not None:
            if self.input_format not in self.possible_formats:
                raise ExpectedException ('Invalid input format. Please select from [%s]' \
                         %', '.join(self.possible_formats))
        else:
            valid_formats = []
            first_file = self.input_files[0]
            first_file.seek(0)
            for converter_name, converter in self.converters.items():
                check_success = converter.check_format(first_file)
                first_file.seek(0)
                if check_success: valid_formats.append(converter_name)
            if len(valid_formats) == 0:
                raise ExpectedException('Input format could not be determined. ' +\
                    'Exiting without conversion.')
            elif len(valid_formats) > 1:
                raise ExpectedException('Input format ambiguous in [%s]. '\
                            %', '.join(valid_formats)\
                         +'Please specify an input format.')
            else:
                self.input_format = valid_formats[0]
        self.primary_converter = self.converters[self.input_format]
        if len(self.input_files) > 1:
            for f in self.input_files[1:]:
                if not self.primary_converter.check_format(f):
                    raise ExpectedException('Inconsistent file types')
                else:
                    f.seek(0)
        self.logger.info('input format: %s' %self.input_format)

    def _open_output_files (self):
        """ Open .crv .crs and .crm output files, plus .err file.
            
            .crv .crs and .crm files are opened using a CravatWriter. 
            .err file will contain all errors which occur during conversion.
            .map file contains two columns showing which lines in input
            correspond to which lines in output.
        """
        # Setup CravatWriter
        self.wpath = os.path.join(self.output_dir,
                                  self.output_base_fname + '.crv')
        self.crv_writer = CravatWriter(self.wpath)
        self.crv_writer.add_columns(constants.crv_def)
        self.crv_writer.write_definition()
        for index_columns in constants.crv_idx:
            self.crv_writer.add_index(index_columns)
        self.crv_writer.wf.write('#input_format={}\n'.format(self.primary_converter.format_name))
        # Setup err file
        self.err_path = os.path.join(self.output_dir,
                                     self.output_base_fname + '.converter.err')
        # Setup crm line mappings file
        self.crm_path = os.path.join(self.output_dir, self.output_base_fname +'.crm')
        self.crm_writer = CravatWriter(self.crm_path)
        self.crm_writer.add_columns(constants.crm_def)
        self.crm_writer.write_definition()
        for index_columns in constants.crm_idx:
            self.crm_writer.add_index(index_columns)
        self.crm_writer.write_input_paths(self.input_path_dict)
        # Setup crs sample file
        self.crs_path = os.path.join(self.output_dir, self.output_base_fname +'.crs')
        self.crs_writer = CravatWriter(self.crs_path)
        self.crs_writer.add_columns(constants.crs_def)
        if hasattr(self.primary_converter, 'addl_cols'):
            self.crs_writer.add_columns(self.primary_converter.addl_cols, append=True)
            constants.crs_def.extend(self.primary_converter.addl_cols)
        self.crs_writer.write_definition()
        for index_columns in constants.crs_idx:
            self.crs_writer.add_index(index_columns)
        # Setup liftover var file
        if self.do_liftover:
            self.crl_path = '.'.join([self.output_base_fname,self.input_assembly,'var'])
            self.crl_writer = CravatWriter(self.crl_path)
            assm_crl_def = copy.deepcopy(constants.crl_def)
            assm_crl_def[1]['title'] = 'Chrom'.format(self.input_assembly.title())
            assm_crl_def[2]['title'] = 'Position'.format(self.input_assembly.title())
            assm_crl_def[2]['desc'] = 'Position in {0}'.format(self.input_assembly.title())
            self.crl_writer.add_columns(assm_crl_def)
            self.crl_writer.write_definition()
            self.crl_writer.write_names(self.input_assembly,
                                        self.input_assembly.title(),
                                        '')

    def run(self):
        """ Convert input file to a .crv file using the primary converter."""
        self.setup()
        start_time = time.time()
        self.status_writer.queue_status_update('status', 'Started {} ({})'.format('Converter', self.primary_converter.format_name))
        last_status_update_time = time.time()
        multiple_files = len(self.input_files) > 1
        fileno = 0
        total_lnum = 0
        for f in self.input_files:
            fileno += 1
            self.primary_converter.setup(f)
            f.seek(0)
            read_lnum = 0
            write_lnum = 0
            num_errors = 0
            for l in f:
                cur_fname = os.path.basename(f.name)
                samp_prefix = cur_fname
                read_lnum += 1
                total_lnum += 1
                try:
                    # all_wdicts is a list, since one input line can become
                    # multiple output lines
                    all_wdicts = self.primary_converter.convert_line(l)
                    if all_wdicts is None:
                        continue
                except Exception as e:
                    num_errors += 1
                    self._log_conversion_error(read_lnum, l, e)
                    continue
                if all_wdicts:
                    UIDMap = [] 
                    for wdict_no in range(len(all_wdicts)):
                        wdict = all_wdicts[wdict_no]
                        chrom = wdict['chrom']
                        if chrom is not None:
                            if not chrom.startswith('chr'): chrom = 'chr' + chrom
                            wdict['chrom'] = self.chromdict.get(chrom, chrom)
                            if multiple_files:
                                if wdict['sample_id']:
                                    wdict['sample_id'] = '__'.join([samp_prefix, wdict['sample_id']])
                                else:
                                    wdict['sample_id'] = samp_prefix
                            if wdict['ref_base'] == '' and wdict['alt_base'] not in ['A','T','C','G']:
                                num_errors += 1
                                e = BadFormatError('Reference base required for non SNV')
                                self._log_conversion_error(read_lnum, l, e)
                                continue
                            if self.do_liftover:
                                prelift_wdict = copy.copy(wdict)
                                try:
                                    wdict['chrom'], wdict['pos'] = self.liftover(wdict['chrom'], wdict['pos'])
                                except LiftoverFailure as e:
                                    num_errors += 1
                                    self._log_conversion_error(read_lnum, l, e)
                                    continue
                            unique, UID = self.vtracker.addVar(wdict['chrom'], int(wdict['pos']), wdict['ref_base'], wdict['alt_base'])                       
                            wdict['uid'] = UID
                            if unique:
                                write_lnum += 1
                                self.crv_writer.write_data(wdict)
                                if self.do_liftover:
                                    prelift_wdict['uid'] = UID
                                    self.crl_writer.write_data(prelift_wdict)
                                self.primary_converter.addl_operation_for_unique_variant(wdict, wdict_no)
                            if UID not in UIDMap: 
                                #For this input line, only write to the .crm if the UID has not yet been written to the map file.   
                                self.crm_writer.write_data({'original_line': read_lnum, 'tags': wdict['tags'], 'uid': UID, 'fileno': self.input_path_dict2[f.name]})
                                UIDMap.append(UID)
                        self.crs_writer.write_data(wdict)
            cur_time = time.time()
            if total_lnum % 10000 == 0 or cur_time - last_status_update_time > 3:
                self.status_writer.queue_status_update('status', 'Running {} ({}): line {}'.format('Converter', cur_fname, read_lnum))
                last_status_update_time = cur_time
        self.logger.info('error lines: %d' %num_errors)
        self._close_files()
        if self.status_writer is not None:
            self.status_writer.queue_status_update('num_input_var', total_lnum)
            self.status_writer.queue_status_update('num_unique_var', write_lnum)
            self.status_writer.queue_status_update('num_error_input', num_errors)
        end_time = time.time()
        self.logger.info('finished: %s' %\
            time.asctime(time.localtime(end_time)))
        runtime = round(end_time - start_time, 3)
        self.logger.info('num input lines: {}'.format(total_lnum))
        self.logger.info('runtime: %s'%runtime)
        self.status_writer.queue_status_update('status', 'Finished {} ({})'.format('Converter', self.primary_converter.format_name))
        return total_lnum, self.primary_converter.format_name

    def liftover(self, old_chrom, old_pos):
        new_coords = self.lifter.convert_coordinate(old_chrom, int(old_pos))
        if new_coords != None and len(new_coords) > 0:
            new_chrom = new_coords[0][0]
            new_pos = new_coords[0][1]
            return new_chrom, new_pos
        else:
            raise LiftoverFailure('Liftover failure')

    def _log_conversion_error(self, ln, line, e):
        """ Log exceptions thrown by primary converter.
            All exceptions are written to the .err file with the exception type
            and message. Exceptions are also written to the log file once, with the 
            traceback. 
        """
        err_str = traceback.format_exc().rstrip()
        if err_str not in self.unique_excs:
            self.unique_excs.append(err_str)
            self.logger.error(err_str)
        self.error_logger.error('\nLINE:{:d}\nINPUT:{}\nERROR:{}\n#'.format(ln, line[:-1], str(e)))

    def _close_files(self):
        """ Close the input and output files. """
        for f in self.input_files:
            f.close()
        self.crv_writer.close()
        self.crm_writer.close()
        self.crs_writer.close()

def main ():
    master_cravat_converter = MasterCravatConverter()
    master_cravat_converter.run()
    
if __name__ ==  '__main__':
    master_cravat_converter = MasterCravatConverter()
    master_cravat_converter.run()
