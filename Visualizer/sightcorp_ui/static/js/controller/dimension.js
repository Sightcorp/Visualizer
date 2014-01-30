var chartTypeValues = {
    S:{
        text:"Simple chart",
        style:"zaxis_simple"
    },
    T:{
        text:"Stacked chart",
        style:"zaxis_stacked"
    }
};

var yAxisValues = {
    NP:{
        text:"Number of Persons",
        axis_text:"Number of Persons"
    }//,
    //NI:{
    //    text:"Number of Shots",
    //    axis_text:"Number of Shots"
    //}
};

var xAxisValues = {
    H:{
        text:"per Hour of Day",
        axis_text:"Hour of Day"
    },
    D:{
        text:"per Day",
        axis_text:"Day"
    },
    C:{
        text:"per Camera",
        axis_text:"Camera"
    },
    GEN:{
        text:"per Gender",
        axis_text:"Gender"
    },
    AGE:{
        text:"per Age",
        axis_text:"Age"
    },
    MOOD:{
        text:"per Mood",
        axis_text:"Mood"
    },
    HAP:{
        text:"per Happy Level",
        axis_text:"Happy Level"
    },
    DIS:{
        text:"per Disgusted Level",
        axis_text:"Disgusted Level"
    },
    ANG:{
        text:"per Angry Level",
        axis_text:"Angry Level"
    },
    SUR:{
        text:"per Surprised Level",
        axis_text:"Surprised Level"
    },
    AFR:{
        text:"per Afraid Level",
        axis_text:"Afraid Level"
    },
    SAD:{
        text:"per Sad Level",
        axis_text:"Sad Level"
    }
};

var zAxisValues = {//type must match a chartType value
    NONE:{
        text:"Not displayed",
        type:"S"
    },
    H:{
        text:"stacked over Hours of Day",
        type:"T"
    },
    C:{
        text:"stacked over Camera",
        type:"T"
    },
    MOOD:{
        text:"stacked over Mood",
        type:"T"
    },
    GEN:{
        text:"stacked over Gender",
        type:"T"
    },
    AGE:{
        text:"stacked over Age",
        type:"T"
    },
    HAP:{
        text:"stacked over Happy Level",
        type:"T"
    },
    DIS:{
        text:"stacked over Disgusted Level",
        type:"T"
    },
    ANG:{
        text:"stacked over Angry Level",
        type:"T"
    },
    SUR:{
        text:"stacked over Surprised Level",
        type:"T"
    },
    AFR:{
        text:"stacked over Afraid Level",
        type:"T"
    },
    SAD:{
        text:"stacked over Sad Level",
        type:"T"
    }
};

DimensionController = function () {
    var allowedCombinations = [
        {t:"S", y:"NP", x:"H", z:''},
        {t:"S", y:"NP", x:"D", z:''},
        {t:"S", y:"NP", x:"C", z:''},
        {t:"S", y:"NP", x:"MOOD", z:''},
        {t:"S", y:"NP", x:"GEN", z:''},
        {t:"S", y:"NP", x:"AGE", z:''},
        {t:"S", y:"NP", x:"HAP", z:''},
        {t:"S", y:"NP", x:"DIS", z:''},
        {t:"S", y:"NP", x:"ANG", z:''},
        {t:"S", y:"NP", x:"SUR", z:''},
        {t:"S", y:"NP", x:"AFR", z:''},
        {t:"S", y:"NP", x:"SAD", z:''},

        {t:"T", y:"NP", x:"H", z:'C'},
        {t:"T", y:"NP", x:"H", z:'MOOD'},
        {t:"T", y:"NP", x:"H", z:'GEN'},
        {t:"T", y:"NP", x:"H", z:'AGE'},
        {t:"T", y:"NP", x:"H", z:'HAP'},
        {t:"T", y:"NP", x:"H", z:'DIS'},
        {t:"T", y:"NP", x:"H", z:'ANG'},
        {t:"T", y:"NP", x:"H", z:'SUR'},
        {t:"T", y:"NP", x:"H", z:'AFR'},
        {t:"T", y:"NP", x:"H", z:'SAD'},

        {t:"T", y:"NP", x:"D", z:'H'},
        {t:"T", y:"NP", x:"D", z:'C'},
        {t:"T", y:"NP", x:"D", z:'MOOD'},
        {t:"T", y:"NP", x:"D", z:'GEN'},
        {t:"T", y:"NP", x:"D", z:'AGE'},
        {t:"T", y:"NP", x:"D", z:'HAP'},
        {t:"T", y:"NP", x:"D", z:'DIS'},
        {t:"T", y:"NP", x:"D", z:'ANG'},
        {t:"T", y:"NP", x:"D", z:'SUR'},
        {t:"T", y:"NP", x:"D", z:'AFR'},
        {t:"T", y:"NP", x:"D", z:'SAD'},

        {t:"T", y:"NP", x:"C", z:'H'},
        {t:"T", y:"NP", x:"C", z:'D'},
        {t:"T", y:"NP", x:"C", z:'MOOD'},
        {t:"T", y:"NP", x:"C", z:'GEN'},
        {t:"T", y:"NP", x:"C", z:'AGE'},
        {t:"T", y:"NP", x:"C", z:'HAP'},
        {t:"T", y:"NP", x:"C", z:'DIS'},
        {t:"T", y:"NP", x:"C", z:'ANG'},
        {t:"T", y:"NP", x:"C", z:'SUR'},
        {t:"T", y:"NP", x:"C", z:'AFR'},
        {t:"T", y:"NP", x:"C", z:'SAD'},

        {t:"T", y:"NP", x:"MOOD", z:'H'},
        {t:"T", y:"NP", x:"MOOD", z:'D'},
        {t:"T", y:"NP", x:"MOOD", z:'C'},
        {t:"T", y:"NP", x:"MOOD", z:'GEN'},
        {t:"T", y:"NP", x:"MOOD", z:'AGE'},
        {t:"T", y:"NP", x:"MOOD", z:'HAP'},
        {t:"T", y:"NP", x:"MOOD", z:'DIS'},
        {t:"T", y:"NP", x:"MOOD", z:'ANG'},
        {t:"T", y:"NP", x:"MOOD", z:'SUR'},
        {t:"T", y:"NP", x:"MOOD", z:'AFR'},
        {t:"T", y:"NP", x:"MOOD", z:'SAD'},

        {t:"T", y:"NP", x:"GEN", z:'H'},
        {t:"T", y:"NP", x:"GEN", z:'D'},
        {t:"T", y:"NP", x:"GEN", z:'C'},
        {t:"T", y:"NP", x:"GEN", z:'MOOD'},
        {t:"T", y:"NP", x:"GEN", z:'GEN'},
        {t:"T", y:"NP", x:"GEN", z:'AGE'},
        {t:"T", y:"NP", x:"GEN", z:'HAP'},
        {t:"T", y:"NP", x:"GEN", z:'DIS'},
        {t:"T", y:"NP", x:"GEN", z:'ANG'},
        {t:"T", y:"NP", x:"GEN", z:'SUR'},
        {t:"T", y:"NP", x:"GEN", z:'AFR'},
        {t:"T", y:"NP", x:"GEN", z:'SAD'},

        {t:"T", y:"NP", x:"AGE", z:'H'},
        {t:"T", y:"NP", x:"AGE", z:'D'},
        {t:"T", y:"NP", x:"AGE", z:'C'},
        {t:"T", y:"NP", x:"AGE", z:'MOOD'},
        {t:"T", y:"NP", x:"AGE", z:'GEN'},
        {t:"T", y:"NP", x:"AGE", z:'HAP'},
        {t:"T", y:"NP", x:"AGE", z:'DIS'},
        {t:"T", y:"NP", x:"AGE", z:'ANG'},
        {t:"T", y:"NP", x:"AGE", z:'SUR'},
        {t:"T", y:"NP", x:"AGE", z:'AFR'},
        {t:"T", y:"NP", x:"AGE", z:'SAD'},

        {t:"T", y:"NP", x:"HAP", z:'H'},
        {t:"T", y:"NP", x:"HAP", z:'D'},
        {t:"T", y:"NP", x:"HAP", z:'C'},
        {t:"T", y:"NP", x:"HAP", z:'MOOD'},
        {t:"T", y:"NP", x:"HAP", z:'GEN'},
        {t:"T", y:"NP", x:"HAP", z:'AGE'},
        {t:"T", y:"NP", x:"HAP", z:'DIS'},
        {t:"T", y:"NP", x:"HAP", z:'ANG'},
        {t:"T", y:"NP", x:"HAP", z:'SUR'},
        {t:"T", y:"NP", x:"HAP", z:'AFR'},
        {t:"T", y:"NP", x:"HAP", z:'SAD'},

        {t:"T", y:"NP", x:"DIS", z:'H'},
        {t:"T", y:"NP", x:"DIS", z:'D'},
        {t:"T", y:"NP", x:"DIS", z:'C'},
        {t:"T", y:"NP", x:"DIS", z:'MOOD'},
        {t:"T", y:"NP", x:"DIS", z:'GEN'},
        {t:"T", y:"NP", x:"DIS", z:'AGE'},
        {t:"T", y:"NP", x:"DIS", z:'HAP'},
        {t:"T", y:"NP", x:"DIS", z:'ANG'},
        {t:"T", y:"NP", x:"DIS", z:'SUR'},
        {t:"T", y:"NP", x:"DIS", z:'AFR'},
        {t:"T", y:"NP", x:"DIS", z:'SAD'},

        {t:"T", y:"NP", x:"ANG", z:'H'},
        {t:"T", y:"NP", x:"ANG", z:'D'},
        {t:"T", y:"NP", x:"ANG", z:'C'},
        {t:"T", y:"NP", x:"ANG", z:'MOOD'},
        {t:"T", y:"NP", x:"ANG", z:'GEN'},
        {t:"T", y:"NP", x:"ANG", z:'AGE'},
        {t:"T", y:"NP", x:"ANG", z:'HAP'},
        {t:"T", y:"NP", x:"ANG", z:'DIS'},
        {t:"T", y:"NP", x:"ANG", z:'SUR'},
        {t:"T", y:"NP", x:"ANG", z:'AFR'},
        {t:"T", y:"NP", x:"ANG", z:'SAD'},

        {t:"T", y:"NP", x:"SUR", z:'H'},
        {t:"T", y:"NP", x:"SUR", z:'D'},
        {t:"T", y:"NP", x:"SUR", z:'C'},
        {t:"T", y:"NP", x:"SUR", z:'MOOD'},
        {t:"T", y:"NP", x:"SUR", z:'GEN'},
        {t:"T", y:"NP", x:"SUR", z:'AGE'},
        {t:"T", y:"NP", x:"SUR", z:'HAP'},
        {t:"T", y:"NP", x:"SUR", z:'DIS'},
        {t:"T", y:"NP", x:"SUR", z:'ANG'},
        {t:"T", y:"NP", x:"SUR", z:'AFR'},
        {t:"T", y:"NP", x:"SUR", z:'SAD'},

        {t:"T", y:"NP", x:"AFR", z:'H'},
        {t:"T", y:"NP", x:"AFR", z:'D'},
        {t:"T", y:"NP", x:"AFR", z:'C'},
        {t:"T", y:"NP", x:"AFR", z:'MOOD'},
        {t:"T", y:"NP", x:"AFR", z:'GEN'},
        {t:"T", y:"NP", x:"AFR", z:'AGE'},
        {t:"T", y:"NP", x:"AFR", z:'HAP'},
        {t:"T", y:"NP", x:"AFR", z:'DIS'},
        {t:"T", y:"NP", x:"AFR", z:'ANG'},
        {t:"T", y:"NP", x:"AFR", z:'SUR'},
        {t:"T", y:"NP", x:"AFR", z:'SAD'},

        {t:"T", y:"NP", x:"SAD", z:'H'},
        {t:"T", y:"NP", x:"SAD", z:'D'},
        {t:"T", y:"NP", x:"SAD", z:'C'},
        {t:"T", y:"NP", x:"SAD", z:'MOOD'},
        {t:"T", y:"NP", x:"SAD", z:'GEN'},
        {t:"T", y:"NP", x:"SAD", z:'AGE'},
        {t:"T", y:"NP", x:"SAD", z:'HAP'},
        {t:"T", y:"NP", x:"SAD", z:'DIS'},
        {t:"T", y:"NP", x:"SAD", z:'ANG'},
        {t:"T", y:"NP", x:"SAD", z:'SUR'},
        {t:"T", y:"NP", x:"SAD", z:'AFR'}
    ];

    loadDefaultZoneC();

    function loadDefaultZoneC() {
        bindZoneC();
        disableInvalidCombinations();
    }

    function bindZoneC() {
        //when chart type changes
        $('#chart_type').change(function () {
            var chartType = $(this).prop("value");
            updateAxis('t', chartType);
            if (chartType == 'S') {
                updateAxis('z', '');
            } else if (chartType == 'T') {
                updateAxis('z', 'H');
            } //else if (chartType == 'B') {
            //    updateAxis('z', 'H');
            //} 

            disableInvalidCombinations();
            zoneBcontroller.refreshZoneB();
        });

        //when y axis changes
        $('#yaxis').change(function () {
            updateAxis('y', $(this).prop("value"));
            disableInvalidCombinations();

            //if a simple chart is displayed
            if (parameters['t'].toUpperCase() == 'S') {
                //we know there is a global variable called controller that is the VisualizationController
                zoneBcontroller.draw(null, parameters);
            } else {
                zoneBcontroller.refreshZoneB();
            }
            zoneDcontroller.refreshFilters();
        });

        //when x axis changes
        $('#xaxis').change(function () {
            updateAxis('x', $(this).prop("value"));
            disableInvalidCombinations();
            zoneBcontroller.refreshZoneB()
        });

        //when z axis changes
        $("#zaxis").change(function () {
            updateAxis('z', $(this).prop("value"));
            disableInvalidCombinations();
            zoneBcontroller.refreshZoneB()
        });

        $("#save-viz").on('click', function() {
            reportController.saveVizParameters();
        });
    }

    function disableInvalidCombinations() {
        //select defaults for Z Axis based on Chart Type
        var T = parameters['t'].toUpperCase();
        var X = parameters['x'].toUpperCase();
        var Y = parameters['y'].toUpperCase();
        var Z = parameters['z'].toUpperCase();

        if (!isCombinationValid({t:T, y:Y, x:X, z:Z})) {
            updateToDefault(T);

            T = parameters['t'].toUpperCase();
            X = parameters['x'].toUpperCase();
            Y = parameters['y'].toUpperCase();
            Z = parameters['z'].toUpperCase();
        }

        $('#chart_type').html('');
        $.each(chartTypeValues, function (key, value) {
            $('#chart_type').append('<option value="' + key + '" ' + isParameterSelected('t', key) + '>' + value.text + '</option>')
        });

        $('#yaxis').html('');
        $.each(yAxisValues, function (key, value) {
            $('#yaxis').append('<option value="' + key + '" ' + isParameterSelected('y', key) + '>' + value.text + '</option>');
            $("#yaxis option[value='" + key + "']").attr('disabled', !isCombinationValid({t:T, y:key, x:X, z:Z}));
        });

        $('#xaxis').html('');
        $.each(xAxisValues, function (key, value) {
            $('#xaxis').append('<option value="' + key + '" ' + isParameterSelected('x', key) + '>' + value.text + '</option>');
            $("#xaxis option[value='" + key + "']").attr('disabled', !isCombinationValid({t:T, y:Y, x:key, z:Z}));
        });

        $('#zaxis').html('');
        $.each(zAxisValues, function (key, value) {
            if (T == value.type) {
                $('.zaxis').attr('class', 'options zaxis ' + chartTypeValues[value.type].style);
                $('#zaxis').append('<option value="' + key + '" ' + isParameterSelected('z', key) + '>' + value.text + '</option>');
                $("#zaxis option[value='" + key + "']").attr('disabled', !isCombinationValid({t:T, y:Y, x:X, z:key}));
            }
        });
    }

    function updateToDefault(t) {
        var defaultC = $.grep(allowedCombinations, function (v) {
            return t == v.t;
        })[0];
        updateAxis('x', defaultC.x);
        updateAxis('y', defaultC.y);
        updateAxis('z', defaultC.z);
    }

    function isParameterSelected(axis, value) {
        if (parameters[axis].toUpperCase() == value) {
            return 'selected';
        }
        return '';
    }

    function isCombinationValid(comb) {
        var found = false;
        $.each(allowedCombinations, function (k, v) {
            if (comb.t === v.t && comb.y === v.y && comb.x === v.x && comb.z === v.z) {
                found = true;
            }
        });
        return found;
    }
};
