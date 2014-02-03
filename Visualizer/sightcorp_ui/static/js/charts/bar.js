function bar_chart(filterId, data, legend, msg) {
    $('#' + filterId).html('');

    //if no one is selected, select all.
    var all_sel = 1;
    for (var d = 0; d < data.length; d++) {
        if (data[d][2] == 1) {
            all_sel = 0;
            break;
        }
    }

    //margin
    var m = {top:10, right:40, bottom:50, left:10 };

    //chart height, width
    var bar_width = 15;
    if (data.length < 20) bar_width = 25;
    var h = 150;
    var w = bar_width * (data.length + 1);

    var maxY = d3.max(data, function (d) {
        return d[1];
    });

    //add the 'All' option
    data.unshift(['All', maxY, all_sel]);

    if (filterId == 'f_vt') {
        //move Discarded (video_type = 4) as first column, and we assume is always present
        var discardedIndex = -1;
        $.each(data, function(idx, item) {
            if (item[0] == 4) {
                discardedIndex = idx;
            }
        });
        data.splice(0, 0, data[discardedIndex]);
        data.splice(discardedIndex + 1, 1);
    }

    //get x label content
    var xdomain = data.map(function (d) {
        return d[0];
    });

    //create svg
    //set chart position, height, width, etc.
    var chart = d3.select("#" + filterId).append("svg")
        .attr("class", "chart")
        .attr("width", w + m.right + m.left)
        .attr("height", h + m.top + m.bottom);

    //create the set of small bars reflecting data
    var small_bars = chart.append("g").attr("transform", "translate(50,0)");

    var label_margin = 2;
    var label_height = 32;

    //to make clickable area bigger we would also create large bars that do not show the amount like small_bars
    var large_bars = chart.append("g").attr("transform", "translate(50," + label_margin + ")");

    //scale y, flip range to get correct y axis, -10 to make the smallest
    //bar show up at least 10
    var y = d3.scale.linear()
        .domain([0, maxY])
        .range([h, 0]);

    //scale x for xlabels
    var x = d3.scale.ordinal()
        .domain(xdomain)
        .rangeRoundBands([0, w], .1, 0);

    //toggle color
    var toggleSelected = (function (i) {
        //get current color of all bars
        var currentColor = data.map(function (d) {
            return d[2];
        });
        //set currently changed color
        return function (i) {
            currentColor[i] = currentColor[i] == 0 ? 1 : 0;
            if (i != 0)
                currentColor[0] = 0;
            return currentColor;
        }
    })();

    //draw rects
    small_bars.selectAll("rect.bar").data(data).enter()
        .append("rect")
        .attr("x", function (d) {
            if (filterId == 'f_c' || filterId == 'f_d' || filterId == 'f_h'){
                return x(d[0]) + (0.25 * x.rangeBand()) + 3;
            } else if (filterId == 'f_mood' || filterId == 'f_gen'){
                return x(d[0]) + (0.25 * x.rangeBand());// - 3;
            }
            else {
                return x(d[0]) + (0.25 * x.rangeBand());// - 10;
            }
        })
        .attr("y", function (d) {
            return y(d[1]);
        })
        .attr("height", function (d) {
            return h - y(d[1]);
        })
        .attr("width", 0.5 * x.rangeBand())
        .attr('class', function (d, i) {
            return 'bar_' + i;
        })
        .classed('all', function (d) {
            return (d[0] == 'All');
        })
        .classed('bar', true)
        .classed('selected', function (d, i) {
            return d[2];
        })
        .style('stroke-width', '1');

    large_bars.selectAll("rect.surr_box").data(data).enter()
        .append("rect")
        //.attr("x", x)
        .attr("x", function (d) {
            if(d[0] != 'All'){
                if(filterId == 'f_c' || filterId == 'f_d' || filterId == 'f_h'){
                    return x(d[0]) + (0.25 * x.rangeBand());
                } else if(filterId == 'f_mood' || filterId == 'f_gen'){
                    return x(d[0]) + (0.25 * x.rangeBand()) - 4;
                } else {
                    return x(d[0]) + (0.25 * x.rangeBand()) - 5;
                }
            } else {
                if(filterId == 'f_c' || filterId == 'f_d' || filterId == 'f_h'){
                    return x(d[0]) + (0.25 * x.rangeBand());
                } else if(filterId == 'f_mood' || filterId == 'f_gen'){
                    return x(d[0]) + (0.25 * x.rangeBand()) - 10;
                } else {
                    return x(d[0]) + (0.25 * x.rangeBand()) - 15;
                }      
            }
        })
        .attr("y", -label_margin)
        .attr("height", function () {
            if (filterId == "f_c") return h + 21;
            else return h + label_height;
        })
        .attr("width", x.rangeBand())
        .attr('class', function (d, i) {
            return 'bar_' + i;
        })
        .classed('all', function (d) {
            return (d[0] == 'All');
        })
        .classed('surr_box', true)
        .classed('selected', function (d, i) {
            return d[2];
        })
        .style('stroke-width', '1')
        .on('click', function (d, i) {
            var allBarIndex = 0;
            if (filterId == 'f_vt') {
                allBarIndex = 1;
            }

            //if "All" or one of components is selected
            if (i == allBarIndex) {
                //de-select all others
                small_bars.selectAll('rect.bar').classed('selected', false);
                large_bars.selectAll('rect.surr_box').classed('selected', false);
            } else {
                //for other filters, if one of them is selected, deselect All
                small_bars.selectAll('rect.bar_' + allBarIndex).classed('selected', false);
                large_bars.selectAll('rect.bar_' + allBarIndex).classed('selected', false);
            }
            //get colors for all rects
            selects = toggleSelected(i);

            //set the color for changed rect
            small_bars.selectAll('rect.bar_' + i).classed('selected', selects[i]);
            large_bars.selectAll('rect.bar_' + i).classed('selected', selects[i]);

            //set "All" if nothing is selected, or current rect if it's comp filter
            var all_select = true;
            selects.forEach(function (c) {
                if (c == 1)
                    all_select = false;
            });
            if (all_select) {
                large_bars.selectAll('rect.bar_' + allBarIndex).classed('selected', true);
            }

            //then send the request to server to change line chart in zone B
            var changed_value = d[0];
            var add = selects[i] != 0;

            updateFilter(filterId, changed_value, add, true);
            var current_tab = $('#active_tab').val();
            if (current_tab == 'vis' || current_tab == 'vid') {
                zoneBcontroller.refreshZoneB();
                zoneDcontroller.refreshFilters();
            }
        });

    //create labels
    if (filterId == "f_c__DISABLED") {
        var last_camera_in_location = [];
        $.each(legend, function () {
            var temp = [];
            temp.push(this.toString().split(',')[0]);
            var length = this.toString().split(',').length - 1;
            temp.push(this.toString().split(',').length - 1);
            temp.push(this.toString().split(',')[length]);
            last_camera_in_location.push(temp);
        });

        large_bars.selectAll("text").data(data)
            .enter().append("text")
            .attr("x", function (d) {
                return x(d[0]) + x.rangeBand() - (bar_width/6);
            })
            .attr("y", h - label_margin)
            .attr("class", "labels")
            .text(function (d) {
                return d[0]
            })
            .attr("transform", function (d) {
                return "rotate(-90," + (x(d[0]) + x.rangeBand() - (bar_width/6)) + "," + (h + label_margin) +")";
            });

        chart.append("line")
            .attr("x1", 145)
            .attr("y1", h + label_height)
            .attr("x2", 145)
            .attr("y2", 0)
            .style("stroke", "rgb(153,153,153)");
        chart.append("line")
            .attr("x1", 242)
            .attr("y1", h + label_height)
            .attr("x2", 242)
            .attr("y2", 0)
            .style("stroke", "rgb(153,153,153)");
        chart.append("text")
            .attr("x", 90)
            .attr("y", h + label_height)
            .text("HoBiHu");
        chart.append("text")
            .attr("x", 165)
            .attr("y", h + label_height)
            .text("NPP-3");
        chart.append("text")
            .attr("x", 245)
            .attr("y", h + label_height)
            .text("LanYu");

        large_bars.selectAll("rect.bar_0").attr("height", h + label_margin + label_height);
    } else {
        large_bars.selectAll("text").data(data)
            .enter().append("text")
            .attr("x", function (d) {
                return x(d[0]) + x.rangeBand() - (bar_width/4);
            })
//            .attr("y", h + label_margin)
            .attr("y", function(){    
                if(filterId == 'f_c' || filterId == 'f_d' || filterId == 'f_h'){
                    return h + label_margin + 3;
                } else if(filterId == 'f_mood' || filterId == 'f_gen'){
                    return h + label_margin - 7;
                } else {
                    return h + label_margin - 13;
                }
            })
            .attr("class", "labels")
            .text(function (d) {
                if (filterId == 'f_vt' && d[0] != 'All') {
                    return video_type_names[d[0]];
                } else {
                    return d[0]
                }
            })
            .attr("transform", function (d) {
                return "rotate(-90," + (x(d[0]) + x.rangeBand() - (bar_width/4)) + "," + (h + label_margin) +")";
            });
    }

    if (filterId == "f_s") {
        generate_species_legend('f_s_legend', legend);
    }

    if (msg) {
         $('#' + filterId).append('<div class="bar_message">' + msg + '</div>' );
        // chart.append("text")
        //     .attr("x", (w + m.right + m.left)/2)
        //    .attr("y", (h + m.top)/2)
        //    .attr("class", "bar_message").text(msg);
    }
}

function generate_species_legend(div_id, data) {
    var fishbase = new Array();
    fishbase[1] = 'http://fishbase.org/summary/Dascyllus-reticulatus.html';
    fishbase[2] = 'http://fishbase.org/summary/Chromis-margaritifer.html';
    fishbase[3] = 'http://fishbase.org/summary/Plectroglyphidodon-dickii.html';
    fishbase[4] = 'http://fishbase.org/summary/Acanthurus-nigrofuscus.html';
    fishbase[5] = 'http://fishbase.org/summary/Myripristis-berndti.html';
    fishbase[6] = 'http://fishbase.org/summary/Chaetodon-trifascialis.html';
    fishbase[7] = 'http://fishbase.org/summary/Zebrasoma-scopas.html';
    fishbase[8] = 'http://fishbase.org/summary/Scolopsis-bilineata.html';
    fishbase[9] = 'http://fishbase.org/summary/Amphiprion-clarkii.html';
    fishbase[10] = 'http://fishbase.org/summary/Siganus-fuscescens.html';
    fishbase[11] = 'http://fishbase.org/summary/Pomacentrus-amboinensis.html';
    fishbase[13] = 'http://fishbase.org/summary/Calotomus-zonarchus.html';
    fishbase[17] = 'http://fishbase.org/summary/Canthigaster-valentini.html';
    fishbase[19] = 'http://fishbase.org/summary/Balistapus-undulatus.html';
    fishbase[21] = 'http://fishbase.org/summary/Hemigymnus-melapterus.html';
    fishbase[24] = 'http://fishbase.org/summary/Hemigymnus-fasciatus.html';
    fishbase[26] = 'http://fishbase.org/summary/Abudefduf-vaigiensis.html';
    fishbase[27] = 'http://fishbase.org/summary/Lutjanus-fulvus.html';
    fishbase[31] = 'http://fishbase.org/summary/Chaetodon-lunulatus.html';
    fishbase[33] = 'http://fishbase.org/summary/Neoniphon-sammara.html';
    fishbase[34] = 'http://fishbase.org/summary/Pempheris-vanicolensis.html';
    fishbase[36] = 'http://fishbase.org/summary/Arothron-hispidus.html';
    fishbase[37] = 'http://fishbase.org/summary/Zanclus-cornutus.html';
    fishbase[38] = 'http://fishbase.org/summary/Neoglyphidodon-nigroris.html';

    var content = new Array();
   // content.push('<table>');
    for (var i = 0; i < data.length; i++) {
        var fish_image_url = static_url + 'images/species/';
        fish_image_url += data[i][0] + '.' + data[i][1].toLowerCase().replace(' ', '_').replace('-', '_').trim() + '.png';
        content.push('<a href="' + fishbase[data[i][0]] + '" target="_blank" style="text-decoration:none;color:#666;"><table><tr>');
        content.push('<td>' + data[i][0] + '</td>');
        content.push('<td><img src="' + fish_image_url + '"></td>');
        content.push('<td>' + data[i][1] + '</td>');
        content.push('</a></td></tr></table>')
    }
    //content.push('</table>');
    $('#' + div_id).html(content.join(''));
}
