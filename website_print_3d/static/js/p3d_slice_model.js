odoo.define('website.slice_model', ['web.ajax'], function (require) {
    "use strict";

    var filename = '';
    var Ajax = require('web.ajax');
    var showMessage = function (data) {
        $("#slicing_status").append('<p class="message"><b>' + data + '</p>');
        //for JSON
        // for (var x in data) {
        //     $("#slicing_status").append('<p class="message"><b>' + data[x] + '</p>');
        // }
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
            var ws = new WebSocket("ws://10.0.0.40:5000/slicing/status/Hex_Rook"), data;
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
            };
            var messageFile = "Uploading file" + filename + " to Server ...";
            showMessage(messageFile);

            Ajax.post($(this).attr("action"), form_values).then(function (data) {
                //http://10.0.0.40:7136
                showMessage(data);
                $("iframe[name='PGCodeViewerFrame']").attr('src', 'http://10.0.0.40:7136');
                $("div[class*='js_cart_summary']").show();
                $("a[href*='/shop/checkout']").removeClass("disabled");
                setTimeout(function(){
                    $("iframe[name='PGCodeViewerFrame']").contentWindow.window.uploadGcode("http://10.0.0.40:5000/files/gcode/Hex_Queen.gcode");
                    }, 10000);
            });
        });
    });
});
