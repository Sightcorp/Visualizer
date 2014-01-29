var zoneBcontroller;
var zoneCcontroller;
var zoneDcontroller;

var number_asynchronous_calls = 0;

$(document).ready(function () {

    //set up ajax for django
    $.ajaxSetup({
        beforeSend:function (xhr, settings) {
            number_asynchronous_calls++;

            //show loading gif if the request takes longer then 500
            setTimeout(function () {
                if ($.active > 0) {
                    $("#loading_image").show();
                }
            }, 500);

            function getCookie(name) {
                var cookieValue = null;
                if (document.cookie && document.cookie != '') {
                    var cookies = document.cookie.split(';');
                    for (var i = 0; i < cookies.length; i++) {
                        var cookie = jQuery.trim(cookies[i]);
                        // Does this cookie string begin with the name we want?
                        if (cookie.substring(0, name.length + 1) == (name + '=')) {
                            cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                            break;
                        }
                    }
                }
                return cookieValue;
            }

            if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
                // Only send the token to relative URLs i.e. locally.
                xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
            }
        },
        complete:function () {
            number_asynchronous_calls--;
            if (number_asynchronous_calls == 0) {
                $("#loading_image").hide();
            }
        }
    });

    $("#dialog").dialog({
        autoOpen:false,
        closeOnEscape:true,
        height:"auto"
    });

    syncInterfaceWithParameters();

    var current_tab = $('#active_tab').val();
    if (current_tab == 'vis') {
        zoneBcontroller = new VizController();
        zoneCcontroller = new DimensionController();
        zoneDcontroller = new FilterController();
        reportController = new ReportController();
    } else if (current_tab == 'vid') {
        zoneBcontroller = new VideoController();
        zoneDcontroller = new FilterController();
    } else if (current_tab == 'vidana') {
        zoneBcontroller = new WorkflowController();
    } else if (current_tab == 'report') {
        reportController = new ReportController();
    }
});

function showDialog(title, text) {
    $('#dialog').dialog('option', 'title', title);
    $('#dialog').text(text);
    $('#dialog').dialog('open');
}