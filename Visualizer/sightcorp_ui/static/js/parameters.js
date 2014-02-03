function addOpenedFilter(filterId) {
    //console.log(JSON.stringify(['add opened filter: ', filterId]));
    parameters['f'].push(filterId);
    syncInterfaceWithParameters();
}

function removeOpenedFilter(filterId) {
    //console.log(JSON.stringify(['remove opened filter: ', filterId]));
    parameters['f'].splice($.inArray(filterId, parameters['f']), 1);
    syncInterfaceWithParameters();
}

function updateAxis(axis, value) {
    //console.log(JSON.stringify(['update axis: ', axis, value]));
    parameters[axis] = value;
    syncInterfaceWithParameters();
}

function updateFilter(filterId, value, add, sync) {
    //console.log(JSON.stringify(['update filter: ', filterId, value, add]));
    if (value == 'All') {
        parameters[filterId] = ['all'];
    } else if (add) {
        //if 'all' is in there empty the array first
        if ($.inArray('all', parameters[filterId]) > -1) {
            parameters[filterId] = [];
        }
        if ($.inArray(value, parameters[filterId]) == -1) {
            parameters[filterId].push(value);
        }
    } else if (!add) {
        if ($.inArray(value, parameters[filterId]) > -1) {
            parameters[filterId].splice($.inArray(value, parameters[filterId]), 1);
        }
        //if there is no value selected, select 'all' automatically
        if (parameters[filterId].length == 0) {
            parameters[filterId] = ['all'];
        }
    }
    if (sync) {
        syncInterfaceWithParameters();
    }
}

function syncInterfaceWithParameters() {
    updateTabsUrl();
    updateFiltersSummary();
}

function updateTabsUrl() {
    var parametersToUrl = addParametersToUrl('');
    $('.zonea_tab').each(function (i, t) {
        var url = t.href;
        if (t.href.indexOf('?') != -1) {
            url = t.href.substring(0, t.href.indexOf('?'));
        }
        t.href = url + parametersToUrl;
    });
    window.history.replaceState(parameters, null, parametersToUrl);
}

function addParametersToUrl(url) {
    var res = url + '?';
    $.each(parameters, function (p) {
        if (!$.isArray(parameters[p])) {
            res = res + p + '=' + parameters[p] + '&';
        } else if (($.isArray(parameters[p]) && parameters[p].length > 0)) {
            res = res + p + '=' + parameters[p].join(',') + '&';
        }
    });
    return res;
}

function updateFiltersSummary() {
    var title="";
    if ($.inArray('all', parameters['f_d']) == -1) {
        var days = $.map(parameters['f_d'], function(day) {return day});
        title += '<div class="title_param_box">on Day <span class="title_param_value">' + days + '<div class="cancel_filter" filter-id="f_d"></div></span></div>';
    }
    if ($.inArray('all', parameters['f_h']) == -1) {
        var hours = $.map(parameters['f_h'], function(hour) {return hour + ':00'});
        title += '<div class="title_param_box"> at <span class="title_param_value">' + hours + '<div class="cancel_filter" filter-id="f_h"></div></span></div>';
    }
    if ($.inArray('all', parameters['f_c']) == -1) {
        title += '<div class="title_param_box"> at <span class="title_param_value">Camera ' + parameters['f_c'] + '<div class="cancel_filter" filter-id="f_c"></div></span></div>';
    }
    if ($.inArray('all', parameters['f_mood']) == -1) {
        pval = '';
        aval = parameters['f_mood'];
        for(i=0; i < aval.length; i++){
            max = aval[i] + 10;
            if(i!=0){
                pval += ', ';
            }
            pval += '[' + aval[i] + ',' + max + ']';
        }
        title += '<div class="title_param_box"> with <span class="title_param_value">Mood in ' + pval + '<div class="cancel_filter" filter-id="f_mood"></div></span></div>';
    }
    if ($.inArray('all', parameters['f_age']) == -1) {
        pval = '';
        aval = parameters['f_age'];
        for(i=0; i < aval.length; i++){
            max = aval[i] + 10;
            if(i!=0){
                pval += ', ';
            }
            pval += '[' + aval[i] + ',' + max + ']';
        }
        title += '<div class="title_param_box"> for <span class="title_param_value">Age in ' + pval +'<div class="cancel_filter" filter-id="f_age"></div></span></div>';
    }
    if ($.inArray('all', parameters['f_gen']) == -1) {
        pval = '';
        aval = parameters['f_gen'];
        for(i=0; i < aval.length; i++){
            max = aval[i] + 10;
            if(i!=0){
                pval += ', ';
            }
            pval += '[' + aval[i] + ',' + max + ']';
        }
        title += '<div class="title_param_box"> for <span class="title_param_value">Gender in ' + pval + '<div class="cancel_filter" filter-id="f_gen"></div></span></div>';
    }
    if ($.inArray('all', parameters['f_hap']) == -1) {
        pval = '';
        aval = parameters['f_hap'];
        for(i=0; i < aval.length; i++){
            max = aval[i] + 10;
            if(i!=0){
                pval += ', ';
            }
            pval += '[' + aval[i] + ',' + max + ']';
        }
        title += '<div class="title_param_box"> <span class="title_param_value">Happy in ' + pval + '<div class="cancel_filter" filter-id="f_hap"></div></span></div>';
    }
    if ($.inArray('all', parameters['f_dis']) == -1) {
        pval = '';
        aval = parameters['f_dis'];
        for(i=0; i < aval.length; i++){
            max = aval[i] + 10;
            if(i!=0){
                pval += ', ';
            }
            pval += '[' + aval[i] + ',' + max + ']';
        }
        title += '<div class="title_param_box"> for <span class="title_param_value">Disgusted in ' + pval + '<div class="cancel_filter" filter-id="f_dis"></div></span></div>';
    }
    if ($.inArray('all', parameters['f_ang']) == -1) {
        pval = '';
        aval = parameters['f_ang'];
        for(i=0; i < aval.length; i++){
            max = aval[i] + 10;
            if(i!=0){
                pval += ', ';
            }
            pval += '[' + aval[i] + ',' + max + ']';
        }
        title += '<div class="title_param_box"> for <span class="title_param_value">Angry in ' + pval + '<div class="cancel_filter" filter-id="f_ang"></div></span></div>';
    }
    if ($.inArray('all', parameters['f_sur']) == -1) {
        pval = '';
        aval = parameters['f_sur'];
        for(i=0; i < aval.length; i++){
            max = aval[i] + 10;
            if(i!=0){
                pval += ', ';
            }
            pval += '[' + aval[i] + ',' + max + ']';
        }
        title += '<div class="title_param_box"> for <span class="title_param_value">Surprised in ' + pval + '<div class="cancel_filter" filter-id="f_sur"></div></span></div>';
    }
    if ($.inArray('all', parameters['f_afr']) == -1) {
        pval = '';
        aval = parameters['f_afr'];
        for(i=0; i < aval.length; i++){
            max = aval[i] + 10;
            if(i!=0){
                pval += ', ';
            }
            pval += '[' + aval[i] + ',' + max + ']';
        }
        title += '<div class="title_param_box"> for <span class="title_param_value">Afraid in ' + pval + '<div class="cancel_filter" filter-id="f_afr"></div></span></div>';
    }
    if ($.inArray('all', parameters['f_sad']) == -1) {
        pval = '';
        aval = parameters['f_sad'];
        for(i=0; i < aval.length; i++){
            max = aval[i] + 10;
            if(i!=0){
                pval += ', ';
            }
            pval += '[' + aval[i] + ',' + max + ']';
        }
        title += '<div class="title_param_box"> for <span class="title_param_value">Sad in ' + pval + '<div class="cancel_filter" filter-id="f_sad"></div></span></div>';
    }
    
    title += '</span>';
    $('#filters_summary').html(title);

    $('.cancel_filter').click(function () {
        var filterId = $(this).attr('filter-id');
        updateFilter(filterId, 'All', false, true);
        zoneBcontroller.refreshZoneB();
        zoneDcontroller.refreshFilters();
    });
}
