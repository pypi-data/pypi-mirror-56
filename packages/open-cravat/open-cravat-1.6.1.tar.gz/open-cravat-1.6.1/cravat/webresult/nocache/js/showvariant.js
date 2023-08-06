function getWidgetTableFrame () {
	var table = getEl('table');
	table.style.fontSize = '12px';
	table.style.borderSpacing = '0px';
	table.style.borderCollapse = 'collapse';
	table.style.borderTop = widgetTableBorderStyle;
	table.style.borderBottom = widgetTableBorderStyle;
	table.style.tableLayout = 'fixed';
	table.style['word-break'] = 'break-all';
	table.style.width = 'calc(100% - 0px)';
	table.style['table-layout'] = 'fixed';
	return table;
}

function getWidgetTableHead (headers, widths) {
	var thead = getEl('thead');
	thead.style.textAlign = 'left';
	thead.style['word-break'] = 'normal';
	thead.style.borderBottom = widgetTableBorderStyle;
	var tr = getEl('tr');
	var numBorder = headers.length - 1;
	for (var i = 0; i < headers.length; i++) {
		var th = getEl('th');
		if (i < numBorder) {
			th.style.borderRight = widgetTableBorderStyle;
		}
		if (widths != undefined){
			th.style.width = widths[i];
		}
		addEl(th, getTn(headers[i]));
		addEl(tr, th);
	}
	addEl(thead, tr);
	return thead;
}

function getWidgetTableTr (values,linkNames) {
	var numBorder = values.length - 1;
	var linkNameItr = 0;
	var tr = getEl('tr');
	tr.style.borderBottom = '1px solid #cccccc';
	for (var i = 0; i < values.length; i++) {
		var td = getEl('td');
		var p = getEl('p');
		if (i < numBorder) {
			td.style.borderRight = widgetTableBorderStyle;
		}
		var value = values[i];
		if (value == null) {
			value = '';
		}
		if(typeof value == 'string' && value.startsWith('http')){
			spanText = document.createElement('a');
			spanText.href = value;
			spanText.target = '_blank';
			if(linkNames != undefined){
				addEl(td, addEl(spanText, getTn(linkNames[linkNameItr])));
				linkNameItr += 1;
			}
			else{
				addEl(td, addEl(spanText, getTn('View')));
			}
		}
		else{
			addEl(td, addEl(p, getTn(value)));
		}
		addEl(tr, td);
	}
	return tr;
}

function getLineHeader (header) {
	var spanHeader = document.createElement('span');
	spanHeader.appendChild(document.createTextNode('  ' + header + ': '));
	return spanHeader;
}

function addInfoLine (div, row, header, col, tabName, headerMinWidth) {
	var text = infomgr.getRowValue(tabName, row, col);
    var table = getEl('table');
    table.style.fontSize = '12px';
    table.style.borderCollapse = 'collapse';
    var tr = getEl('tr');
    var td = getEl('td');
    td.className = 'detail-info-line-header';
    if (headerMinWidth != undefined) {
        td.style.minWidth = headerMinWidth;
    }
    var h = getLineHeader(header);
    addEl(td, h);
    addEl(tr, td);
    td = getEl('td');
    td.className = 'detail-info-line-content';
    var t = getEl('span');
    t.textContent = text;
    addEl(td, t);
    addEl(tr, td);
    addEl(table, tr);
	addEl(div, table);
}

function addInfoLineText (div, header, text) {
	addEl(div, getLineHeader(header));
	var spanText = document.createElement('span');
	if (text == undefined || text == null) {
		text = '';
	} else {
		var textLengthCutoff = 16;
		if (text.length > textLengthCutoff) {
			spanText.title = text;
			text = text.substring(0, textLengthCutoff) + '...';
		}
	}
	addEl(spanText, getTn(text));
	addEl(div, spanText);
	addEl(div, getEl('br'));
}

function addInfoLineLink (div, header, text, link, trimlen) {
	addEl(div, getLineHeader(header));
	var spanText = null;
	if (link == undefined || link == null) {
		text = '';
		spanText = document.createElement('span');
	} else {
		spanText = document.createElement('a');
		spanText.href = link;
		spanText.target = '_blank';
		if (trimlen > 0) {
			if (text.length > trimlen) {
				spanText.title = text;
				text = text.substring(0, trimlen) + '...';
			}
		}
	}
	addEl(spanText, getTn(text));
	addEl(div, spanText);
	addEl(div, getEl('br'));
}

function addBarComponent (outerDiv, row, header, col, tabName) {
	var cutoff = 0.01;
	var barStyle = {
		"top": 0,
		"height": lineHeight,
		"width": 1,
		"fill": 'black',
		"stroke": 'black',
		"round_edge": 1
	};

	// Value
	var value = infomgr.getRowValue(tabName, row, col);
	if (value == null) {
		value = '';
	} else {
        value = value.toFixed(3);
	}
	
	// Div
	var div = getEl('div');
	div.style.display = 'inline-block';
	div.style.margin = '2px';

	// Header
	addEl(div, addEl(getEl('span'), getTn(header + ': ')));
	addEl(div, addEl(getEl('span'), getTn(value)));
	addEl(div, getEl('br'));
	
	// Paper
	var barWidth = 108;
	var barHeight = 12;
	var lineOverhang = 3;
	var lineHeight = barHeight + (2 * lineOverhang);
	var paperHeight = lineHeight + 4;
	var subDiv = document.createElement('div');
	addEl(div, subDiv);
	subDiv.style.width = (barWidth + 10) + 'px';
	subDiv.style.height = paperHeight + 'px';
	var allele_frequencies_map_config = {};
	var paper = Raphael(subDiv, barWidth, paperHeight);
	
	// Box. Red color maxes at 0.3.
	var box = paper.rect(0, lineOverhang, barWidth, barHeight, 4);
	var c = null;
	if (value != '') {
		c = (1.0 - Math.min(1.0, value / 0.3)) * 255;
	} else {
		c = 255;
	}
	box.attr('fill', 'rgb(255, ' + c + ', ' + c + ')');
	box.attr('stroke', 'black');
	
	// Bar
	if (value != '') {
		var bar = paper.rect(value * barWidth, 0, 1, lineHeight, 1);
		bar.attr('fill', 'black');
		bar.attr('stroke', 'black');
	}
	
	addEl(outerDiv, div);
}

//Default color gradeint is white to red from 0.0 to 1.0
function addGradientBarComponent (outerDiv, row, header, col, tabName, colors={'0.0':[255,255,255],'1.0':[255,0,0]}, minval=0.0, maxval=1.0) {
	var cutoff = 0.01;
	var barStyle = {
		"top": 0,
		"height": lineHeight,
		"width": 1,
		"fill": 'black',
		"stroke": 'black',
		"round_edge": 1
	};

	var dtype = null;
	var orderedPivots = [];
	for (pivot in colors){
		orderedPivots.push(pivot)
	}
	orderedPivots.sort(function(a,b){return a-b})
	
	// Value
	var value = infomgr.getRowValue(tabName, row, col);
	if (value == null) {
		value = '';
	}
	else if(typeof value == 'string'){
		dtype = 'string'
	}
	else {
		value = value.toFixed(3);
	}
	
	// Div
	var div = getEl('div');
	div.style.display = 'inline-block';
	div.style.margin = '2px';

	// Header
	addEl(div, addEl(getEl('span'), getTn(header + ': ')));
	addEl(div, addEl(getEl('span'), getTn(value)));
	addEl(div, getEl('br'));
	if(value !== ''){
		value = parseFloat(value);
	}

	// Paper
	var barWidth = 108;
	var barHeight = 12;
	var lineOverhang = 3;
	var lineHeight = barHeight + (2 * lineOverhang);
	var paperHeight = lineHeight + 4;
	var subDiv = document.createElement('div');
	addEl(div, subDiv);
	subDiv.style.width = (barWidth + 10) + 'px';
	subDiv.style.height = paperHeight + 'px';
	var allele_frequencies_map_config = {};
	var paper = Raphael(subDiv, barWidth, paperHeight);
	
	// Box.
	var box = paper.rect(0, lineOverhang, barWidth, barHeight, 4);
	var c = [];
	if (value !== '') {
		if(value <= orderedPivots[0]){
			var piv = orderedPivots[0];
			c = colors['%s',piv];
		}
		else if(value>=orderedPivots[orderedPivots.length-1]){
			var piv = orderedPivots[orderedPivots.length-1];
			c = colors['%s',piv];
		}
		else{
			var boundColors = {color1:[], color2:[]};
			var boundPivots = [];
			for (var i=0; i<(orderedPivots.length-1); i++){
				if (orderedPivots[i] <= value && value < orderedPivots[i+1]){
					boundPivots[0] = orderedPivots[i];
					boundPivots[1] = orderedPivots[i+1];
					boundColors.color1 = colors[boundPivots[0]];
					boundColors.color2 = colors[boundPivots[1]];
					break;
				}
			}
			//semi-broken when values are negative
			var ratio = (value - boundPivots[0])/(boundPivots[1]-boundPivots[0]);
			c[0] = Math.round(boundColors.color1[0] * (1.0 - ratio) + boundColors.color2[0] * ratio);
			c[1] = Math.round(boundColors.color1[1] * (1.0 - ratio) + boundColors.color2[1] * ratio);
			c[2] = Math.round(boundColors.color1[2] * (1.0 - ratio) + boundColors.color2[2] * ratio);
		}
		
	} else {
		c = [255, 255, 255];
	}
	box.attr('fill', 'rgb('+c.toString()+')');
	box.attr('stroke', 'black');
	
	// Bar
	if (value !== '' && dtype != 'string') {
		//Convert values onto 0 to 1 scale depending on min and max val provided (defaults to 0 and 1)
		value = (value - parseFloat(minval))/(Math.abs(parseFloat(minval)) + Math.abs(parseFloat(maxval)));
		var bar = paper.rect(value * barWidth, 0, 1, lineHeight, 1);
		bar.attr('fill', 'black');
		bar.attr('stroke', 'black');
	}
	
	addEl(outerDiv, div);
}

function showVariantDetail (row, tabName) {
	if (row == undefined) {
		return;
	}
	
	var detailDiv = document.getElementById('detaildiv_' + tabName);
	if (! detailDiv) {
		return;
	}
	var outerDiv = detailDiv.getElementsByClassName('detailcontainerdiv')[0];
	$outerDiv = $(outerDiv);

	// Remembers widget layout.
	var widgetDivs = outerDiv.children;
	var reuseWidgets = true;
	if (widgetDivs.length == 0) {
		reuseWidgets = false;
	} else {
		widgetDivs = $(outerDiv).packery('getItemElements');
	}
	if (reuseWidgets == true) {
		detailWidgetOrder[tabName] = {};
		for (var i = 0; i < widgetDivs.length; i++) {
			var widgetDiv = widgetDivs[i];
			var widgetKey = widgetDiv.getAttribute('widgetkey');
			detailWidgetOrder[tabName][i] = widgetKey;
			widgetGenerators[widgetKey]['width'] = widgetDiv.clientWidth - 10;
			widgetGenerators[widgetKey]['height'] = widgetDiv.clientHeight - 10;
			widgetGenerators[widgetKey]['top'] = widgetDiv.style.top;
			widgetGenerators[widgetKey]['left'] = widgetDiv.style.left;
		}
	}

	if (tabName == 'error'){
		return
	}
	
	var scrollTop = outerDiv.scrollTop;
		
	var orderNums = Object.keys(detailWidgetOrder[tabName]);
	for (var i = 0; i < orderNums.length; i++) {
		var colGroupKey = detailWidgetOrder[tabName][orderNums[i]];
        try {
            if (widgetGenerators[colGroupKey] == undefined) {
                continue;
            }
            var colGroupTitle = infomgr.colgroupkeytotitle[colGroupKey];
            if (colGroupTitle == undefined) {
                colGroupTitle = widgetGenerators[colGroupKey]['name'];
            }
            if (widgetGenerators[colGroupKey][tabName] != undefined && 
                widgetGenerators[colGroupKey][tabName]['function'] != undefined) {
                var generator = widgetGenerators[colGroupKey][tabName];
                var widgetDiv = null;
                var detailContentDiv = null;
                var shouldDraw = false;
                if (generator['shoulddraw'] != undefined) {
                    shouldDraw = generator['shoulddraw']();
                } else {
                    shouldDraw = true;
                }
                if (reuseWidgets) {
                    widgetContentDiv = document.getElementById(
                        'widgetcontentdiv_' + colGroupKey + '_' + tabName);
                    if (generator['donterase'] != true) {
                        $(widgetContentDiv).empty();
                    }
                    if (shouldDraw) {
                        generator['function'](widgetContentDiv, row, tabName);
                    }
                } else {
                    [widgetDiv, widgetContentDiv] = 
                        getDetailWidgetDivs(tabName, colGroupKey, colGroupTitle);
                    generator['variables']['parentdiv'] = widgetContentDiv;
                    if (generator['init'] != undefined) {
                        generator['init']();
                    }
                    widgetDiv.style.width = generator['width'] + 'px';
                    widgetDiv.style.height = generator['height'] + 'px';
                    addEl(outerDiv, widgetDiv);
                    if (shouldDraw) {
                        generator['function'](widgetContentDiv, row, tabName);
                    }
                    var setting = getViewerWidgetSettingByWidgetkey(tabName, colGroupKey);
                    if (setting != null) {
                        var display = setting['display'];
                        if (display != undefined) {
                            widgetDiv.style.display = display;
                        }
                    }
                }
            }
        } catch (err) {
            console.log(err);
            console.log('### exception while drawing widget [' + colGroupKey + '] continuing to the next widget ###');
        }
	}
	if (reuseWidgets == false) {
		$outerDiv.packery({
			columnWidth: widgetGridSize,
			rowHeight: widgetGridSize
		});
		var $widgets = $($outerDiv.packery('getItemElements'));
		$widgets.draggable({
			grid: [widgetGridSize, widgetGridSize],
			handle: '.detailwidgettitle',
            stop: function (evt, ui) {
                $outerDiv.packery();
                loadedViewerWidgetSettings[currentTab] = undefined;
            },
		}).resizable({
			grid: [widgetGridSize, widgetGridSize],
            start: function (evt, ui) {
                var widgetName = evt.target.getAttribute('widgetkey');
                var generator = widgetGenerators[widgetName][tabName];
                var v = generator['variables'];
                var parentDiv = v['parentdiv'];
                if (generator['beforeresize'] != undefined) {
                    generator['beforeresize']();
                }
            },
            stop: function (evt, ui) {
                var widgetName = evt.target.getAttribute('widgetkey');
                var generator = widgetGenerators[widgetName][tabName];
                var v = generator['variables'];
                var widgetContentDiv = v['parentdiv'];
                var row = $grids[tabName].pqGrid('getData')[selectedRowNos[tabName]];
                if (generator['donterase'] != true) {
                    $(widgetContentDiv).empty();
                }
                generator['variables']['resized'] = true;
                if (generator['confirmonresize'] == true) {
                    var div = getEl('div');
                    div.className = 'widget-redraw-confirm';
                    var span = getEl('span');
                    span.textContent = 'Click to redraw';
                    addEl(div, span);
                    addEl(widgetContentDiv, div);
                    div.addEventListener('click', function () {
                        generator['function'](widgetContentDiv, row, tabName);
                        $outerDiv.packery('fit', ui.element[0]);
                    });
                } else {
                    generator['function'](widgetContentDiv, row, tabName);
                    $outerDiv.packery('fit', ui.element[0]);
                }
                var sEvt = evt;
                var sUi = ui;
                $(sEvt.target.parentElement).packery('fit', sUi.element[0]);
                loadedViewerWidgetSettings[currentTab] = undefined;
            },
		});
		$outerDiv.packery('bindUIDraggableEvents', $widgets);
		var resizeTimeout;
		$outerDiv.on('layoutComplete', onLayoutComplete);
	}
	for (var i = 0; i < orderNums.length; i++) {
		var colGroupKey = detailWidgetOrder[tabName][orderNums[i]];
        if (widgetGenerators[colGroupKey] == undefined) {
            continue;
        }
        var widgetDiv = document.getElementById(
            'detailwidget_' + tabName + '_' + colGroupKey);
        var display = widgetDiv.style.display;
        if (widgetGenerators[colGroupKey][tabName] != undefined) {
            var generator = widgetGenerators[colGroupKey][tabName];
            if (generator['showhide'] != undefined) {
                var state = generator['showhide']();
                var widgetContainerDiv = document.getElementById('widgetcontentdiv_' + colGroupKey + '_' + tabName);
                if (state == false) {
                    var span = getEl('span');
                    addEl(span, getTn('No data'));
                    addEl(widgetContainerDiv, span);
                } else if (state == true) {
                }
            }
        }
    }
}


function onLayoutComplete () {
    if (viewerWidgetSettings[currentTab] == undefined) {
        return;
    }
	for (var i = 0; i < viewerWidgetSettings[currentTab].length; i++) {
		var setting = viewerWidgetSettings[currentTab][i];
		var el = document.getElementById(setting.id);
		if (el) {
			el.style.top = setting.top;
			el.style.left = setting.left;
			el.style.width = setting.width;
			el.style.height = setting.height;
            el.style.display = setting.display;
			viewerWidgetSettings[currentTab].splice(i, 1);
			i--;
		}
	}
}
