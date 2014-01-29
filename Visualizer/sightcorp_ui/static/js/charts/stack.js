function StackChart(chart, chart_size, transitionTimeout, controller) {
    var xScale, yScale;

    var controlsMargins = {left:15, right:0};
    var controlsHeight = 27;
    var offsetOptions = {
        Stacked:'zero',
        Expanded:'expand',
        Stream:'wiggle'
    };
    var offsetStatus = 'Stacked';

    var color = d3.scale.category20()
        .domain(function (d) {
            return d.key;
        });

    var area;

    this.scales = function (dataset) {
        var stack = d3.layout.stack()
            .offset(offsetOptions[offsetStatus])
            .values(function (d) {
                return d.values;
            })
            .x(function (d) {
                return d[0];
            })
            .y(function (d) {
                return d[1];
            });

        stack(dataset);

        var allValues = [];
        $.each(dataset, function (index, value) {
            allValues = allValues.concat(value.values);
        });

        var xExtent = d3.extent(allValues, function (d) {
            return d[0];
        });
        xScale = d3.scale.linear().domain(xExtent).range([0, chart_size.width]);

        var yMax = d3.max(allValues, function (d) {
            return d.y + d.y0;
        });
        yScale = d3.scale.linear().domain([0, yMax]).range([chart_size.height, controlsHeight]);

        return {x:xScale, y:yScale};
    };

    this.draw = function (dataset) {
        area = d3.svg.area()
            .x(function (d) {
                return xScale(d[0]);
            })
            .y0(function (d) {
                return yScale(d.y0);
            })
            .y1(function (d) {
                return yScale(d.y0 + d.y);
            });

        exit(dataset);
        transition(dataset);
        enter(dataset);

        drawInteractivePoints(dataset);
        drawOffsets();
        drawLegend(dataset);
    };

    this.dispose = function () {
        exit([]);
    };

    function enter(dataset) {
        var pathsGroup = chart.select("g.paths_group");
        if (pathsGroup.empty()) {
            pathsGroup = chart.append("g").attr("class", "paths_group");
        }

        //draws areas
        pathsGroup.selectAll("path.stack_chart_path")
            .data(dataset)
            .enter()
            .append("path")
            .attr("class", function (d) {
                return "stack_chart_path stack_chart_path_" + d.key;
            })
            .attr("d", function (d) {
                return area(d.values);
            })
            .style("fill", function (d) {
                return color(d.key);
            })
            .on("mouseover", function (d) {
                d3.select(this).style("fill-opacity", 1);
                chart.select('#Legend-' + d.key).style('opacity', 1).style('stroke-width', 2);
                chart.select('#Item-Legend-' + d.key).style('opacity', 1);
            })
            .on("mouseout", function (d) {
                d3.select(this).style("fill-opacity", 0.6);
                chart.select('#Legend-' + d.key).style("opacity", 0.6).style('stroke-width', 0);
                chart.select('#Item-Legend-' + d.key).style('opacity', 0.4);
            });
    }

    function transition(dataset) {
        //upgrades areas
        chart.selectAll("path.stack_chart_path")
            .data(dataset)
            .transition()
            .duration(transitionTimeout)
            .attr("class", function (d) {
                return "stack_chart_path stack_chart_path_" + d.key;
            })
            .attr("d", function (d) {
                return area(d.values);
            })
            .style("fill", function (d) {
                return color(d.key);
            });
    }

    function exit(dataset) {
        //removes areas
        chart.selectAll("path.stack_chart_path")
            .data(dataset)
            .exit()
            .transition()
            .duration(transitionTimeout)
            .attr("opacity", 0)
            .remove();

        if (dataset.length == 0) {
            chart.select("g.interactive_points").remove();
            chart.select("g.stack_chart_offset").remove();
            chart.select("g.stack_chart_legend").remove();
        }
    }

    function drawInteractivePoints(dataset) {
        var interactivePoints = chart.select("g.interactive_points");
        if (interactivePoints.empty()) {
            interactivePoints = chart.append("g").attr("class", "interactive_points");
        }

        //aggregate all points for computing Voronoi tessellation
        var groupedPoints = [];
        var uniquePoints = [];
        $.each(dataset, function (stackIndex, stack) {
            var stackKey = stack.key;
            $.each(stack.values, function (pointIndex, point) {
                var x = xScale(point[0]);
                var y = yScale(point.y0 + point.y);
                var scaledPoint = [x, y];

                var found = false;
                var uniquePointIndex = uniquePoints.length;
                $.each(uniquePoints, function (samePointIndex, v3) {
                    //consolidating coincident vertices otherwise the distribution will have problem
                    if (v3[0] == x && v3[1] == y) {
                        uniquePointIndex = samePointIndex;
                        found = true;
                        return false;
                    }
                });
                if (!found) {
                    uniquePoints.push(scaledPoint);
                    groupedPoints[uniquePointIndex] = {};
                    groupedPoints[uniquePointIndex].keys = [stackKey];
                    groupedPoints[uniquePointIndex].value = point.y0 + point.y;
                } else {
                    groupedPoints[uniquePointIndex].keys.push(stackKey);
                }
            });
        });

        var voronoiDistribution = d3.geom.voronoi(uniquePoints);

        //Reset and draw clips
        var pointClips = interactivePoints.select("#point-clips");
        if (pointClips.empty()) {
            pointClips = interactivePoints.append("g").attr("id", "point-clips");
        } else {
            pointClips.selectAll(".clipclass").remove();
        }
        pointClips.selectAll("clipPath")
            .data(uniquePoints)
            .enter()
            .append("clipPath")
            .attr('class', 'clipclass')
            .attr("id", function (d, i) {
                return "clip-" + i;
            })
            .append("circle")
            .attr('cx', function (d) {
                return d[0];
            })
            .attr('cy', function (d) {
                return d[1];
            })
            .attr('r', 10);

        //Reset and draw interaction paths
        var pointPaths = interactivePoints.select('#point-paths');
        if (pointPaths.empty()) {
            pointPaths = interactivePoints.append("g").attr("id", "point-paths");
        } else {
            pointPaths.selectAll("path").remove();
        }
        pointPaths.selectAll("path")
            .data(voronoiDistribution)
            .enter()
            .append("path")
            .attr("d", function (d) {
                return "M" + d.join(",") + "Z";
            })
            .attr("id", function (d, i) {
                return "path-" + i;
            })
            .attr("clip-path", function (d, i) {
                return "url(#clip-" + i + ")";
            })
            .style("fill", d3.rgb(230, 230, 230))
            .style('fill-opacity', 0)
            .style("stroke", d3.rgb(200, 200, 200))
            .style("stroke-opacity", 0)
            .on("mouseover", function (d, i) {
                d3.select(this)
                    .style('fill', d3.rgb(31, 120, 180))
                    .style('fill-opacity', 0.5);

                var point = interactivePoints.select('circle#point-' + i);
                point.transition().attr('r', 2);
                controller.showTooltip(point, groupedPoints[i].value, d3.select('#yLabel').text());

                $.each(groupedPoints[i].keys, function (i, key) {
                    chart.select('.stack_chart_path_' + key).style('fill-opacity', 1);
                    chart.select('#Legend-' + key).style('opacity', 1).style('stroke-width', 2);
                    chart.select('#Item-Legend-' + key).style('opacity', 1);
                });
            })
            .on("mouseout", function (d, i) {
                d3.select(this)
                    .style("fill", d3.rgb(230, 230, 230))
                    .style('fill-opacity', 0);

                interactivePoints.select('circle#point-' + i).transition().attr('r', 0);
                controller.hideTooltip();

                $.each(groupedPoints[i].keys, function (i, key) {
                    chart.select('.stack_chart_path_' + key).style('fill-opacity', 0.6);
                    chart.select('#Legend-' + key).style('opacity', 0.6).style('stroke-width', 0);
                    chart.select('#Item-Legend-' + key).style('opacity', 0.4);
                });
            });

        //draws, updates and removes points
        var points = interactivePoints.select("#points");
        if (points.empty()) {
            points = interactivePoints.append("g").attr("id", "points");
        }
        points.selectAll("circle")
            .data(uniquePoints)
            .enter()
            .append("circle")
            .attr("id", function (d, i) {
                return "point-" + i;
            })
            .attr("cx", function (d) {
                return d[0];
            })
            .attr("cy", function (d) {
                return d[1];
            })
            .attr("r", 0)
            .attr('stroke', 'none')
            .attr("pointer-events", "none")
            .style('fill', 'Red');

        points.selectAll("circle")
            .data(uniquePoints)
            .transition()
            .attr("cx", function (d) {
                return d[0];
            })
            .attr("cy", function (d) {
                return d[1];
            });

        points.selectAll("circle")
            .data(uniquePoints)
            .exit()
            .remove();
    }

    function drawOffsets() {
        var offsetGroup = chart.select("g.stack_chart_offset");
        if (offsetGroup.empty()) {
            offsetGroup = chart.append("g").attr('class', "stack_chart_offset");
        }

        var keys = [];
        for (var k in offsetOptions) keys.push(k);

        var offsetItemWidth = 70;
        offsetGroup.selectAll("circle")
            .data(keys)
            .enter()
            .append("circle")
            .attr('r', 5)
            .attr('cx', function (d, i) {
                return controlsMargins.left + (offsetItemWidth * i);
            })
            .attr('cy', controlsHeight / 4)
            .attr('id', function (d) {
                return 'Offset-' + d;
            })
            .attr('fill-opacity', function (d) {
                if (d == offsetStatus) return 1;
                else return 0;
            })
            .on('click', function (d) {
                syncOffset(d);
            });
        offsetGroup.selectAll("text")
            .data(keys)
            .enter()
            .append('text')
            .text(function (d) {
                return d;
            })
            .attr('dx', function (d, i) {
                return controlsMargins.left + (offsetItemWidth * i) + 7;
            })
            .attr('dy', 11);
    }

    function syncOffset(chosenKey) {
        offsetStatus = chosenKey;
        $.each(offsetOptions, function (key) {
            chart.select('#Offset-' + key).attr('fill-opacity', function () {
                if (key == chosenKey) return 1;
                else return 0;
            })
        });
        controller.draw(null, parameters);
    }

    function drawLegend(dataset) {
        var legendGroup = chart.select("g.stack_chart_legend");
        if (legendGroup.empty()) {
            legendGroup = chart.append("g").attr('class', "stack_chart_legend");
        } else {
            legendGroup.selectAll("image").remove();
            legendGroup.selectAll("text").remove();
            legendGroup.selectAll("circle").remove();
        }

        var legendItemWidth;
        var zAxis = parameters['z'].toUpperCase();
        if (zAxis == 'S') {
            legendItemWidth = 40;
            var legendItemHeight = 18;
            legendGroup.selectAll("image.item")
                .data(dataset)
                .enter()
                .append('image')
                .attr('class', 'item')
                .attr('id', function (d) {
                    return 'Item-Legend-' + d.key;
                })
                .attr("xlink:href", function (d) {
                    return static_url + 'images/species/' + d.key + '.png';
                })
                .attr("width", legendItemWidth)
                .attr("height", legendItemHeight)
                .attr('x', function (d, i) {
                    return chart_size.width - controlsMargins.right - legendItemWidth - (legendItemWidth * i);
                })
                .attr('y', 9)
                .style('opacity', 0.4);
        } else if (zAxis == 'C') {
            legendItemWidth = 58;
            legendGroup.selectAll("text.item")
                .data(dataset)
                .enter()
                .append('text')
                .attr('class', 'item')
                .attr('id', function (d) {
                    return 'Item-Legend-' + d.key;
                })
                .text(function (d) {
                    return 'Camera ' + d.key;
                })
                .attr('dx', function (d, i) {
                    return chart_size.width - controlsMargins.right - (legendItemWidth / 2) - (legendItemWidth * i);
                })
                .attr('dy', 20)
                .style('opacity', 0.4);
        }
        legendGroup.selectAll("circle.elem")
            .data(dataset)
            .enter()
            .append("circle")
            .attr('class', 'elem')
            .attr('r', 8)
            .attr('cx', function (d, i) {
                return chart_size.width - controlsMargins.right - (legendItemWidth / 2) - (legendItemWidth * i);
            })
            .attr('cy', 0)
            .attr('id', function (d) {
                return 'Legend-' + d.key;
            })
            .attr('fill', function (d) {
                return color(d.key);
            });
        legendGroup.selectAll("text.elem")
            .data(dataset)
            .enter()
            .append("text")
            .attr('class', 'elem')
            .attr("dx", function (d, i) {
                return chart_size.width - controlsMargins.right - (legendItemWidth / 2) - (legendItemWidth * i);
            })
            .attr('dy', 4)
            .text(function(d) {
                return d.key;
            });
    }

}