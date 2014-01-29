FilterController = function () {
    var filtersArray = {
        f_c: 'Camera',
        f_d: 'Day',
        f_h: 'Hour of Day',
        f_mood: 'Mood',
        f_gen: 'Gender',
        f_age: 'Age',
        f_hap: 'Happy',
        f_dis: 'Disgusted',
        f_ang: 'Angry',
        f_sur: 'Surprised',
        f_afr: 'Afraid',
        f_sad: 'Sad'
    };

    var zoneDrequestTimer;

    loadDefaultFilters();

    function loadDefaultFilters() {
        //normalize empty filters with 'all'
        $.each(filtersArray, function (key) {
            //// updateFilter(key, 'all', false, false);
            updateFilter(key, 'All', false, false);
        });

        syncInterfaceWithParameters();

        $.ajax({
            type:"GET",
            url:filter_data_url,
            data:parameters
        }).done(function (response) {
                //the response is an array of filters data key = div_id, value=data
                //extra contains things like the species names, as they are too long to be labels in plots
                var filtersId = Object.keys(response);
                for (var i in filtersId) {
                    //console.log('adding filter: ' + filtersId[i]);
                    addFilterHTML(filtersId[i]);
                }
                renderFilters(response);
                updateFiltersSelection();
            }
        );

        bindFilters();
    }

    function bindFilters() {
        // add filter when selecting from the dropdown
        $('#filters_selection').on("change", function () {
            var filterId = $(this).prop("value");
            addOpenedFilter(filterId);
            addFilter(filterId);
        });

        //remove filter when clicking on the cross
        $('body').delegate("div.close_cross", "click", function () {
            var filterId = $(this).closest('li').attr('id');
            if (filterId) {
                //after getting the <li> that contains the filter we need to notify the server using the filterId
                //and to find the filterId we just string the li_ from the <li> id
                deleteFilter(filterId.substring(3));
            }
        });
    }

    this.refreshFilters = function () {
        clearTimeout(zoneDrequestTimer);
        zoneDrequestTimer = setTimeout(function () {
            $.ajax({type:"GET", url:filter_data_url, data:parameters}).done(renderFilters);
        }, 1000);
    };

    function addFilter(filterId) {
        //cloning (deep copying) the parameters object before sending the request for only this filter
        var localParameters = $.extend(true, {}, parameters);
        localParameters['f'] = [filterId];
        $.ajax({
            type:"GET",
            url:filter_data_url,
            data:localParameters
        }).done(
            function (response) {
                $("#filters_selection").val('0');
                addFilterHTML(filterId);
                renderFilters(response);
                updateFiltersSelection();
            }
        );
    }

    function addFilterHTML(filterId) {
        if (isValidFilter(filterId)) {
            var filterElement = "<li id='li_" + filterId + "'><div class='filter_box'>" +
                "<div class='filter_name'>" + filtersArray[filterId] + "</div>" +
                "<div class='close_cross'></div>" +
                "<div class='xaxis_filter_off'></div>" +
                "<div id='" + filterId + "' class='filter_viz'></div>";
            //if (filterId == "f_s") {
            //    filterElement += "<div id='f_s_legend' class='filter_viz'></div>";
            //}
            filterElement += "</div></li>";

            $("#filters_area").prepend(filterElement);
        }
    }

    function renderFilters(response) {
        var filterKeys = [];
        var filterValues = [];

        $.each(response, function (key, value) {
            if (isValidFilter(key)) {
                filterKeys.push(key);
                filterValues.push(value);
            }
        });

        /////////////////////
        /*
        // the camera filter needs data reordering
        if (response['f_c']) {
            var index = $.inArray("f_c", filterKeys);
            filterValues[index] = rearrangeFilterLocationData(filterValues[index], response['f_c_legend']);
        }
        */
        ////////////////////
        $.each(filterKeys, function (index) {
            bar_chart(this, filterValues[index], response[this + '_legend'], response[this + '_msg']);
        });
    }

    function isValidFilter(id) {
        var found = false;
        $.each(filtersArray, function (k) {
            if (id == k) found = true;
        });
        return found;
    }
    /////////////////////
    /*
    function rearrangeFilterLocationData(tempValue, groups) {
        var temp_data = [];
        $.each(groups, function () {
            var temp = this.toString();
            var camera_in_group = temp.split(",");
            $.each(camera_in_group, function () {
                var loc_name = camera_in_group[0];
                var cam = this.toString();
                $.each(tempValue, function () {
                    var temp = this.toString();
                    var camera_info = temp.split(",");
                    if (camera_info[0] == cam) {
                        this.push(loc_name);
                        temp_data.push(this);
                    }
                });
            });
        });
        return temp_data;
    }
    */
    ///////////////////////////

    function deleteFilter(filterId) {
        //console.log('delete filter: ' + filterId);
        $('#li_' + filterId).remove();
        removeOpenedFilter(filterId);
        updateFiltersSelection();
    }

    function updateFiltersSelection() {
        $.each(filtersArray, function (key) {
            if ($('#li_' + key).length > 0) {
                $('#sel_' + key).attr('disabled', true);
            } else {
                $('#sel_' + key).attr('disabled', false);
            }
        });
    }
};
