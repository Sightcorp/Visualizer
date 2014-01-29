function BoxChart(chart, chart_size, transitionTimeout) {
    var xScale, yScale;

    var box_height = chart_size.height;
    var box_width = 10;
    var xPadding = box_width / 2;

    var box = d3.box()
        .whiskers(iqr(1.5))
        .width(box_width)
        .height(box_height);

    this.scales = function(dataset) {
        var xExtent = d3.extent(dataset, function (d) {
            return d[0];
        });
        xScale = d3.scale.linear().domain(xExtent).range([box_width, chart_size.width - box_width]);

        var yMax = d3.max(dataset, function (d) {
            return d[2];
        });
        yScale = d3.scale.linear().domain([0, yMax]).range([chart_size.height, 0]);

        return {x: xScale, y: yScale};
    };

    this.draw = function (dataset) {
        var min = Infinity,
            max = -Infinity;

        var data = [];
        dataset.forEach(function (x) {
            var e = Math.floor(x[0]),
                r = Math.floor(x[1]),
                s = Math.floor(x[2]),
                d = data[e];
            if (!d) d = data[e] = [s];
            else d.push(s);
            if (s > max) max = s;
            if (s < min) min = s;
        });

        box.domain([min, max]);

        //selection
        var selection = chart.selectAll("g.box").data(data);

        //add new data-join elements
        selection.enter()
            .append("g")
            .attr("class", "box")
            .attr("transform", function (d, i) {
                return "translate(" + (xScale(i) - xPadding) + ",0)"
            });

        //update data-join
        selection.call(box.duration(transitionTimeout));
    };

    this.dispose = function () {
        var selection = chart.selectAll("g.box");
        selection.call(box.domain([0, 0]));
        selection.transition().duration(transitionTimeout).remove();
    };

    // Returns a function to compute the interquartile range.
    function iqr(k) {
        return function (d, i) {
            var q1 = d.quartiles[0],
                q3 = d.quartiles[2],
                iqr = (q3 - q1) * k,
                i = -1,
                j = d.length;
            while (d[++i] < q1 - iqr);
            while (d[--j] > q3 + iqr);
            return [i, j];
        };
    }
}