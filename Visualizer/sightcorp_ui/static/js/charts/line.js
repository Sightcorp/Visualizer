function LineChart(chart, chart_size, transitionTimeout,controller) {
    var xScale, yScale;

    this.scales = function (dataset) {
        var index = datasetIndexForYaxis();

        var xExtent = d3.extent(dataset, function (d) {
            return d[0];
        });
        xScale = d3.scale.linear().domain(xExtent).range([0, chart_size.width]);

        var yMax = d3.max(dataset, function (d) {
            return d[index];
        });
        yScale = d3.scale.linear().domain([0, yMax]).range([chart_size.height, 0]);

        return {x:xScale, y:yScale};
    };

    this.draw = function (dataset) {
        exit(dataset);
        transition(dataset);
        enter(dataset);
    };

    this.dispose = function () {
        exit([]);
    };

    function enter(dataset) {
        var index = datasetIndexForYaxis();

        //draws circles
        chart.selectAll("circle.line_chart_circle")
            .data(dataset)
            .enter()
            .append("circle")
            .attr("cx", function (d) {
                return xScale(d[0]);
            })
            .attr("cy", function (d) {
                return yScale(d[index]);
            })
            .attr("r", 0)
            .attr("class", "line_chart_circle")
            .on("mouseover", function (d) {
                var point = d3.select(this);
                point.transition().attr("r", 8);
                controller.showTooltip(point, d[datasetIndexForYaxis()], d3.select('#yLabel').text());
            })
            .on("mouseout", function () {
                d3.select(this).transition().attr("r", 4);

                controller.hideTooltip();
            })
            .transition()
            .duration(transitionTimeout)
            .attr("r", 4);


        //draws path
        if (chart.select("path.line_chart_path").empty()) {
            var line = d3.svg.line()
                .x(function (d) {
                    return xScale(d[0])
                })
                .y(function (d) {
                    return yScale(d[index])
                });
            chart.append("path")
                .attr("d", line(dataset))
                .attr("class", "line_chart_path")
                .attr("opacity", 0)
                .transition()
                .duration(transitionTimeout)
                .attr("opacity", 1);
        }
    }

    function transition(dataset) {
        var index = datasetIndexForYaxis();

        //update circles
        chart.selectAll("circle.line_chart_circle")
            .data(dataset)
            .transition()
            .duration(transitionTimeout)
            .each("start", function () {
                d3.select(this)
                    .attr("class", "line_chart_circle_transition")
                    .attr("r", 6);
            })
            .attr("cx", function (d) {
                return xScale(d[0]);
            })
            .attr("cy", function (d) {
                return yScale(d[index]);
            })
            .each("end", function () {
                d3.select(this)
                    .transition()
                    .duration(1000)
                    .attr("class", "line_chart_circle")
                    .attr("r", 4);
            });

        //update path
        var line = d3.svg.line()
            .x(function (d) {
                return xScale(d[0])
            })
            .y(function (d) {
                return yScale(d[index])
            });
        chart.select("path.line_chart_path")
            .transition()
            .duration(transitionTimeout)
            .attr("d", line(dataset));
    }

    function exit(dataset) {
        //removes circles
        chart.selectAll("circle.line_chart_circle")
            .data(dataset)
            .exit()
            .transition()
            .duration(transitionTimeout)
            .attr("r", 0)
            .remove();

        //removes path
        chart.select("path.line_chart_path")
            .data(dataset)
            .exit()
            .transition()
            .duration(transitionTimeout)
            .attr("opacity", 0)
            .remove();
    }

    function datasetIndexForYaxis() {
        var index;
        var yAxis = parameters['y'].toUpperCase();
        if (yAxis == 'NP') { //person count
            index = 1;
        } else  if (yAxis == 'FC') { //fish raw count
            index = 1;
        } else if (yAxis == 'VC') { //video count
            index = 3;
        } else if (yAxis == 'NFC') { //fish per video
            index = 4;
        } else if (yAxis == 'SC') { //species richness
            index = 5;
        }
        return index;
    }
}