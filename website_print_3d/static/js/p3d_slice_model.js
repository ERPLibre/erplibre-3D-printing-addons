odoo.define('website.slice_model', ['web.ajax'], function (require) {
    "use strict";

    var Ajax = require('web.ajax');
    $(function () {
        $("button#toggleFull").on('click', function () {
            document.querySelector('iframe').requestFullscreen();
        });
        $("input[type='file']").change(function (e) {
            var filename = e.target.files[0].name;
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
            Ajax.post($(this).attr("action"), form_values).then(function (data) {
                alert(data);
            });
        });
    });
});
