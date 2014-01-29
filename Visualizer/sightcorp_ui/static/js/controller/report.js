ReportController = function () {
    loadUserReports();

    function loadUserReports() {
        if ($('#active_tab').val() == 'report') {
            $.ajax({type:"GET", url:user_report}).done(renderReports);

            $('#report_title').on('keyup', function() {
                updateReportTitle();
            });

            $('#download_container').attr('href', user_report_file);
            $('#upload_form').attr('action', user_report_file);

            $('#upload_file').on('change', function(){
                $(this).parent().submit();
            });
        }
    }

    this.saveVizParameters = function () {
        $.ajax({type:"POST", url:user_report, data:{cmd:'save', parameters:JSON.stringify(parameters)}}).done(
            function (response) {
                if (response['duplicate']) {
                    showDialog('Warning', 'NOT Saved! You already have it in the reports.')
                } else {
                    showDialog('Success', 'Chart saved in the reports.')
                }
            }
        );
    };

    function renderReports(response) {
        var report = response['report'];
        $('#report_title').val(report.title);

        $.each(report.charts, function (i, chart) {
            var id = chart.id;
            var params = JSON.parse(chart.parameters);
            var description = chart.description;
            var name = chart.name;
            generateReport(id, params, name, description);
        });
    }

    function generateReport(chartId, params, name, description) {
        var reportContainerId = 'report_container_' + chartId;
        var reportChartId = 'chart_report_' + chartId;
        var removeReportId = 'remove_report_' + chartId;
        var editReportId = 'edit_report_' + chartId;

        var chartNameId = 'chart_name_' + chartId;
        var chartDescriptionId = 'chart_description_' + chartId;

        var html = '' +
            '<div id="' + reportContainerId + '" >' +
            '<div class="report_item" >' +
            '<textarea id="' + chartNameId + '" class="item_title" placeholder="Chart name" rows="2">' + name + '</textarea>' +
            '<div id="' + reportChartId + '" class="report_vis"></div>' +
            '<textarea id="' + chartDescriptionId + '" class="item_description" placeholder="Chart description" rows="11">' + description + '</textarea>' +
            '</div>' +
            '<div class="report_btn">' +
            '<div class="edit_viz" id="' + editReportId + '"><span>Edit<br>Visualization</span></div>' +
            '<div class="remove_item" id="' + removeReportId + '"><span>Remove<br>from Report</span></div>' +
            '</div>';

        $('#report_content').append(html);

        new VizController(reportChartId, 0.5, params);

        $('#' + editReportId).on('click', function () {
            var win = window.open(visualization_url + '?' + $.param(params), '_blank');
            win.focus();
        });

        $('#' + removeReportId).on('click', function () {
            $.ajax({type:"POST", url:user_report, data:{cmd:'remove', id:chartId}}).done(
                $('#'+reportContainerId).remove()
            );
        });

        $('#' + chartNameId).on('keyup', function () {
            updateChart(chartId, chartNameId, chartDescriptionId);
        });

        $('#' + chartDescriptionId).on('keyup', function () {
            updateChart(chartId, chartNameId, chartDescriptionId);
        });
    }

    var reportUpdateTimer;
    function updateReportTitle() {
        clearTimeout(reportUpdateTimer);
        reportUpdateTimer = setTimeout(function() {
            $.ajax({type:"POST", url:user_report, data:{
                cmd:'update-report', title:$('#report_title').val()
            }});
        }, 1000);
    }

    var chartUpdateTimer;
    function updateChart(chartId, chartNameId, chartDescriptionId) {
        clearTimeout(chartUpdateTimer);
        chartUpdateTimer = setTimeout(function() {
            $.ajax({type:"POST", url:user_report, data:{
                cmd:'update-chart', id:chartId, name:$('#' + chartNameId).val(), description:$('#' + chartDescriptionId).val()
            }});
        }, 1000);
    }

};