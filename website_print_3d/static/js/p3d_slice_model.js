odoo.define('website.slice_model', ['web.ajax'], function (require) {
    "use strict";

    var filename = '';
    var Ajax = require('web.ajax');
    var showMessage = function (data) {
        if (typeof data === "object") {
            $("#slicing_status").append('<p class="message">' + data['message'] + '</p>');
            // $("input[type='text']").val(1000);
        } else {
            $("#slicing_status").append('<p class="message">' + data + '</p>');
        }
    }
    $(function () {
        $("button#toggleFull").on('click', function () {
            document.querySelector('iframe').requestFullscreen();
        });
        $("input[type='file']").change(function (e) {
            filename = e.target.files[0].name;
            if (filename.match(/\.(stl|amf|obj)$/)) {
                $("#p3d_slice_model_submit").toggleClass('disabled', !filename);
            } else {
                alert("Incorrect file type. Please choose an STL or OBJ or AMF file!")
            }
        });
        //Submit the form to the SuperSlicer Server
        $("#p3d_slice_model").on('submit', function (e) {
            e.preventDefault();
            var form = $(this);
            var form_array = form.serializeArray();

            var form_values = {};
            _.each(form_array, function (input) {
                if (input.value !== '') {
                    form_values[input.name] = input.value;
                }
            });
            _.each(form.find('input[type=file]'), function (input) {
                $.each($(input).prop('files'), function (index, file) {
                    form_values[input.name] = file;
                });
            });
            var base_name = filename.split('.')[0];
            //Websocket connection : not working as wanted
            /*var ws_url = "ws://127.0.0.1:5000/slicing/status/" + base_name;
            var ws = new WebSocket(ws_url), data;
            ws.onopen = function () {
                console.log("Connected...");
            };
            ws.onmessage = function (event) {
                data = JSON.parse(event.data);
                console.log("New Message", data);
                if (data) showMessage(data);
            };
            ws.onclose = function () {
                console.log("Closed!");
            };*/
            var messageFile = "Uploading file " + filename + " to Server ...";
            showMessage(messageFile);
            var gcode_url = "http://127.0.0.1:5000/files/gcode/" + base_name + ".gcode";

            Ajax.post($(this).attr("action"), form_values).then(function (data) {
                //Display the response text from the SuperSlicer Server
                showMessage(JSON.parse(data));
                //ReActivate the summary and the buttons
                $("div[class*='js_cart_summary']").show();
                $("a[href*='/shop/checkout']").removeClass("disabled");
                //Load the Gcode from the URL
                document.getElementById('iframegcode').contentWindow
                    .postMessage(gcode_url, '*');
            }, function (error) {
                alert(error.statusText);
            });
        });
    });
});
