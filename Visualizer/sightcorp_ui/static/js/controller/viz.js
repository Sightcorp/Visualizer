VizController = function (parentElement, scale, params) {
    var dimensions = {width:1000, height:300};
    var margins = {top:10, right:10, bottom:35, left:60};
    var chart_size = {
        width:dimensions.width - margins.left - margins.right,
        height:dimensions.height - margins.top - margins.bottom
    };

    var transitionTimeout = 1000; //1 sec
    var format = d3.format('8,.1f');

    if (!parentElement) parentElement = "main_chart";
    if (!scale) scale = 1;
    var svg = d3.select('#' + parentElement)
        .append("svg")
        .attr("width", dimensions.width)
        .attr("height", dimensions.height)
        .append("g")
        .attr("transform", "scale(" + scale + "),translate(" + margins.left + "," + margins.top + ")");

    var axes_group = svg.append("g").attr("class", "axes_group");
    var grid_group = svg.append("g").attr("class", "grid_group");
    var chart_group = svg.append("g").attr("class", "chart_group");

    var charts = {
        simple:new LineChart(chart_group, chart_size, transitionTimeout, this),
        stack:new StackChart(chart_group, chart_size, transitionTimeout, this),
        box:new BoxChart(chart_group, chart_size, transitionTimeout)
    };
    var currentChartType;

    if (!params) {
        params = parameters;
        refresh(this);
    } else {
        load(this, params);
    }

    this.refreshZoneB = function () {
        refresh(this);
    };

    var requestTimer;
    function refresh(scope) {
        clearTimeout(requestTimer);
        requestTimer = setTimeout(function () {
            load(scope, params);
        }, 1000);
    }

    function load(scope, data) {
        $.ajax({type:"GET", url:viz_data_url, data:data}).done(
            function (response) {
                renderMainChart.apply(scope, [response, data])
            }
        );
    }

    var chartTypeMapping = {
        S:'simple',
        T:'stack',
        B:'box' 
    };
    function renderMainChart(response, parameters) {
        this.setDataset(response['viz']);
        var chartType = chartTypeMapping[parameters['t'].toUpperCase()];
        this.draw(chartType, parameters);
    }

    this.setDataset = function (dataset) {
        this.data = dataset;
    };

    this.draw = function (chartType, parameters) {
        //cloning (deep copying) the dataset before handing it off to the chart
        var d = $.extend(true, [], this.data);

        if (chartType && chartType != currentChartType) {
            if (currentChartType) charts[currentChartType].dispose();
            currentChartType = chartType;
        }

        var chart = charts[currentChartType];
        var scales = chart.scales(d);
        drawAxes(scales, parameters);
        if (scale == 1) {
            drawGrid(scales);
        }
        chart.draw(d);
    };

    function drawAxes(scales, parameters) {
        var xLabel = xAxisValues[parameters['x'].toUpperCase()].axis_text;
        var yLabel = yAxisValues[parameters['y'].toUpperCase()].axis_text;

        var xTicks = scales.x.domain()[1] - scales.x.domain()[0] + 1;
        var xAxis = d3.svg.axis().scale(scales.x).orient("bottom").ticks(xTicks);
        var yAxis = d3.svg.axis().scale(scales.y).orient("left");

        if (axes_group.select(".x.axis").empty()) {
            axes_group.append("g")
                .attr("class", "x axis")
                .attr("transform", "translate(0," + chart_size.height + ")")
                .call(xAxis);

            axes_group.append("g")
                .attr("class", "y axis")
                .call(yAxis);

            axes_group.select(".x.axis")
                .append("text")
                .text(xLabel)
                .attr("x", chart_size.width / 2)
                .attr("y", margins.bottom - 3)
                .attr("id", "xLabel");

            axes_group.select(".y.axis")
                .append("text")
                .text(yLabel)
                .attr("text-anchor", "middle")
                .attr("transform", "rotate (-270, 0, 0)")
                .attr("x", chart_size.height / 2)
                .attr("y", margins.left - 3)
                .attr("id", "yLabel");
        } else {
            document.getElementById('xLabel').textContent = xLabel;
            axes_group.select(".x.axis")
                .transition()
                .duration(transitionTimeout)
                .call(xAxis);

            document.getElementById('yLabel').textContent = yLabel;
            axes_group.select(".y.axis")
                .transition()
                .duration(transitionTimeout)
                .call(yAxis);
        }
    }

    function drawGrid(scales) {
        var xValues = range(scales.x.domain()[0], scales.x.domain()[1] + 1);
        grid_group.selectAll("line.chart_grid")
            .data(xValues)
            .enter()
            .append("line")
            .attr("class", "chart_grid")
            .attr("x1", function (d) {
                return scales.x(d);
            })
            .attr("x2", function (d) {
                return scales.x(d);
            })
            .attr("y1", scales.y.range()[1])
            .attr("y2", chart_size.height);

        grid_group.selectAll("line.chart_grid")
            .data(xValues)
            .transition()
            .duration(transitionTimeout)
            .attr("x1", function (d) {
                return scales.x(d);
            })
            .attr("x2", function (d) {
                return scales.x(d);
            })
            .attr("y1", scales.y.range()[1]);

        grid_group.selectAll("line.chart_grid")
            .data(xValues)
            .exit()
            .transition()
            .duration(transitionTimeout)
            .attr("y1", chart_size.height)
            .remove();
    }

    function range(start, stop, step) {
        if (typeof stop == 'undefined') {
            // one param defined
            stop = start;
            start = 0;
        }
        if (typeof step == 'undefined') {
            step = 1;
        }
        if ((step > 0 && start >= stop) || (step < 0 && start <= stop)) {
            return [];
        }
        var result = [];
        for (var i = start; step > 0 ? i < stop : i > stop; i += step) {
            result.push(i);
        }
        return result;
    }

    this.showTooltip = function (circle, number, detail) {
        var xPosition = parseFloat(circle.attr('cx')) + margins.left;
        var yPosition = parseFloat(circle.attr('cy')) + 30;
        if (yPosition > chart_size.height) {
            yPosition -= 90;
        }

        var tooltip = d3.select("#tooltip")
            .style("left", xPosition + "px")
            .style("top", yPosition + "px")
            .classed("hidden", false);
        tooltip.select("#tooltip-value")
            .text(format(number));
        tooltip.select('#tooltip-detail')
            .text(detail);
    };

    this.hideTooltip = function () {
        var tooltip = d3.select("#tooltip").classed("hidden", true);
    };
};