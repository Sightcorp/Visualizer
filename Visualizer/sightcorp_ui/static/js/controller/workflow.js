WorkflowController = function () {
    var tabs = ['overview', 'fish_detection', 'fish_recognition', 'workflow'];

    switchTab(tabs[0]); //default overview
    bindWorkflowControls();

    //TODO: mocked cameras data for now
    var camerasData = [
        [40, 1, 0, "HoBiHu"],
        [41, 1, 0, "HoBiHu"],
        [43, 1, 0, "HoBiHu"],
        [37, 1, 0, "NPP-3"],
        [38, 1, 0, "NPP-3"],
        [39, 1, 0, "NPP-3"],
        [42, 1, 0, "NPP-3"],
        [44, 1, 0, "LanYu"],
        [46, 1, 0, "LanYu"]
    ];
    var extrasData = [
        ["HoBiHu", "40,41,43"],
        ["NPP-3", "37,38,39,42"],
        ["LanYu", "44,46"]
    ];
    $.each(camerasData, function (i, v) {
        if ($.inArray(v[0], parameters['f_c']) > -1) {
            v[2] = 1;
        }
    });
    bar_chart('f_c', camerasData, extrasData);

    refresh();

    this.refreshZoneB = function () {
        refresh();
    };

    var RELOAD_TIME = 15 * 1000; //10 sec
    var requestTimer;

    function refresh() {
        clearTimeout(requestTimer);
        $.ajax({type:"GET", url:user_query_url}).done(renderUserQueries);
        requestTimer = setTimeout(function () {
            refresh()
        }, RELOAD_TIME);
    }

    function switchTab(tab) {
        $.each(tabs, function (i, v) {
            if (v == tab) {
                $('#' + v).attr('class', 'visible');
                $('#' + v + '_tab').toggleClass('subtab-active', true);
            } else {
                $('#' + v).attr('class', 'hidden');
                $('#' + v + '_tab').toggleClass('subtab-active', false);
            }
        })
    }

    function bindWorkflowControls() {
        $(".datepicker").datepicker({
            dateFormat:'dd-mm-yy',
            defaultDate:'01-01-2010',
            changeYear:true,
            yearRange:'2010:2011',
            firstDay:1,
            showWeek:true,
            weekHeader:'Week'
        });

        $('#vidana_start_analysis').click(function () {
            submit('add', 'all_fish_species_recognition', renderUserQueries);
        });

        $('#vidana_estimate').click(function () {
            submit('estimate', 'time_estimation_all_fish_species_recognition', watchEstimationQuery);
        });

        $.each(tabs, function (i, tab) {
            $('#' + tab + '_tab').on('click', function () {
                switchTab(tab)
            });
        })
    }

    function submit(command, query, callbackFn) {
        if (checkSubmitWorkflow()) {
            var fishDetection = $('#workflow_detection').prop('value');
            var speciesRecognition = $('#workflow_recognition').prop('value');
            var start = $('#timeframe_start').val();
            var end = $('#timeframe_end').val();
            $.ajax({type:"POST", url:user_query_url, data:{
                cmd:command, q:query, detection:fishDetection, recognition:speciesRecognition, start:start, end:end, f_c:parameters['f_c']
            }}).done(callbackFn);
        }
    }

    function checkSubmitWorkflow() {
        var submit = true;
        var timeRangeStart = new Date(2010, 0, 1);
        var timeRangeEnd = new Date(2011, 11, 31);
        var timeframeStart = $('#timeframe_start').datepicker('getDate');
        if (!timeframeStart || timeframeStart < timeRangeStart || timeframeStart > timeRangeEnd) {
            submit = false;
            showDialog('Warning', 'Cannot insert because the start time is not valid.');
        }
        var timeframeEnd = $('#timeframe_end').datepicker('getDate');
        if (!timeframeEnd || timeframeEnd < timeRangeStart || timeframeEnd > timeRangeEnd) {
            submit = false;
            showDialog('Warning', 'Cannot insert because the end time is not valid.');
        }
        if (timeframeStart > timeframeEnd) {
            submit = false;
            showDialog('Warning', 'Cannot insert because timeframes are overlapping.');
        }
        return submit;
    }

    function renderUserQueries(response) {
        if (response['duplicate']) {
            showDialog('Warning', 'Cannot insert a duplicate analysis.');
        } else {
            var queriesElem = $('#current_queries');
            queriesElem.html('');
            $.each(response['queries'], function (id, query) {
                queriesElem.append(generateSummaryQuery(query));
            });
            var now = new Date();
            $('#queries_list_update_time').html(now.toLocaleTimeString() + ' ' + $.datepicker.formatDate('dd-mm-yy', now));

            $('.abort_query').click(function () {
                var queryId = $(this).attr('id');
                $.ajax({type:"POST", url:user_query_url, data:{
                    cmd:'abort', id:queryId
                }}).done(renderUserQueries);
            });

            if (response['added']) {
                var query_id = response['id'];
                showDialog('Success', 'The analysis ' + query_id + ' has been scheduled.');
            }
            if (response['aborted']) {
                showDialog('Success', 'The analysis ' + query_id + ' has been cancelled.');
            }
        }
    }

    function watchEstimationQuery(response) {
        if (response['duplicate']) {
            showDialog('Warning', 'Cannot insert a duplicate estimation.');
        } else if (response['added']) {
            var estimationQueryId = response['id'];
            showDialog('Success', 'The estimation ' + estimationQueryId + ' has been scheduled.');

            keepWatching(estimationQueryId);

            function keepWatching(estimationQueryId) {
                $.ajax({type:"POST", url:user_query_url, data:{cmd:'estimate_result', id:estimationQueryId}}).done(
                    function (response) {
                        var r = response['result'];
                        if (r == -1) {
                            $('#estimation_result').html('Estimating ...');
                        } else {
                            $('#estimation_result').html('The query can be completed within ' + Math.round(r / 60) + ' minutes');
                        }
                    });
                setTimeout(function () {
                    keepWatching(estimationQueryId)
                }, RELOAD_TIME);
            }
        }
    }

    function generateSummaryQuery(query) {
        var queryId = query['id'];
        var queryStatus = query['status'];

        var html = '<div class="process">';
        html += '<div class="query_id">Q.' + queryId + '</div>';
        html += '<div class="status_' + queryStatus + '"></div>';
        if (queryStatus == 'pending' || queryStatus == 'running') {
            html += '<div class="time_left">' + Math.round(query['time_left'] / 60) + ' min left,</div>';
        }
        html += '<div class="detection_sft">Detection D' + query['detection'] + '</div>';
        if (query['recognition'] != 0) {
            html += '<div class="recognition_sft">Recognition R' + query['recognition'] + '</div>';
        }
        html += '<div class="progress_bar"><div style="width: ' + query['completed'] + '%"></div></div>';
        if (queryStatus == 'pending' || queryStatus == 'running') {
            html += '<div class="close_cross abort_query" id="' + query['id'] + '"></div><div class="message">Cancel</div>';
        }
        html += '</div>';

        return html;
    }

};