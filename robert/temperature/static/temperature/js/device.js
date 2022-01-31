$(document).ready(function()
{
    function getCookie(c_name) {
        if (document.cookie.length > 0) {
            c_start = document.cookie.indexOf(c_name + "=");
            if (c_start != -1) {
                c_start = c_start + c_name.length + 1;
                c_end = document.cookie.indexOf(";", c_start);
                if (c_end == -1) c_end = document.cookie.length;
                return unescape(document.cookie.substring(c_start,c_end));
            }
        }
        return "";
    }
    $(document).on("click", ".statusButton", function()
    {
            console.log('Status Button!')
            let device_id = $(this).attr('device');
            console.log(device_id);
            $.ajax
            ({
                url: '/ajax/change-state/',
                type: 'POST',
                headers: { "X-CSRFToken": getCookie("csrftoken")},
                data: 
                {
                    'device_id': device_id,
                },
                success: function(data) 
                {
                    console.log('SUCCESS!!!!!!!!!!! ' + data.online);
                    if (data.error) 
                    {
                        console.log(data.error);
                    }
                    let status_button_id = "#statusButton-" + device_id;
                    let status_id = "#status-" + device_id;
                    if (data.online == true) 
                    {
                        $(status_button_id).removeClass('btn-success');
                        $(status_button_id).addClass('btn-danger');
                        $(status_button_id).html('Turn off');
                        $(status_id).html('On');
                    }
                    else 
                    {
                        $(status_button_id).removeClass('btn-danger');
                        $(status_button_id).addClass('btn-success');
                        $(status_button_id).html('Turn on');
                        $(status_id).html('Off');
                    }
                },
                error: function(data) 
                {
                    console.log('ERROR!!!!!!!!!!!!');
                }
            });
    });

        $(document).on("click", ".tempButton", function()
        {
            console.log('Temp Button!');
            let device_id = $(this).attr('device');
            let device_temperature = $("#newTemperature-" + device_id).val();
            console.log(device_temperature);
            console.log(device_id);
            $.ajax
            ({
                url: '/ajax/change-temp/',
                type: 'POST',
                headers: { "X-CSRFToken": getCookie("csrftoken")},
                data: 
                {
                    'device_id': device_id,
                    'temperature': device_temperature,
                },
                success: function(data) 
                {
                    console.log('SUCCESS!!!!!!!!!!! ' + data.temperature);
                    if (data.error) 
                    {
                        console.log(data.error);
                    }
                    $('#temperature-' + device_id).html(data.temperature);
                },
                error: function(data) 
                {
                    console.log('ERROR!!!!!!!!!!!!');
                }
            });
        });
})