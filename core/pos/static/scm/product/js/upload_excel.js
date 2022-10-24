document.addEventListener('DOMContentLoaded', function (e) {
    const fv = FormValidation.formValidation(document.getElementById('frmForm'), {
            locale: 'es_ES',
            localization: FormValidation.locales.es_ES,
            plugins: {
                trigger: new FormValidation.plugins.Trigger(),
                submitButton: new FormValidation.plugins.SubmitButton(),
                bootstrap: new FormValidation.plugins.Bootstrap(),
                icon: new FormValidation.plugins.Icon({
                    valid: 'fa fa-check',
                    invalid: 'fa fa-times',
                    validating: 'fa fa-refresh',
                }),
            },
            fields: {
                archive: {
                    validators: {
                        notEmpty: {},
                        callback: {
                            message: 'Introduce un archivo en formato excel',
                            callback: function (input) {
                                var ext = $('input[name="archive"]').val().split('.').pop().toLowerCase();
                                return $.inArray(ext, ['xls', 'xlsx']) !== -1;
                            }
                        },
                    }
                },
            },
        }
    )
        .on('core.element.validated', function (e) {
            if (e.valid) {
                const groupEle = FormValidation.utils.closest(e.element, '.form-group');
                if (groupEle) {
                    FormValidation.utils.classSet(groupEle, {
                        'has-success': false,
                    });
                }
                FormValidation.utils.classSet(e.element, {
                    'is-valid': false,
                });
            }
            const iconPlugin = fv.getPlugin('icon');
            const iconElement = iconPlugin && iconPlugin.icons.has(e.element) ? iconPlugin.icons.get(e.element) : null;
            iconElement && (iconElement.style.display = 'none');
        })
        .on('core.validator.validated', function (e) {
            if (!e.result.valid) {
                const messages = [].slice.call(fv.form.querySelectorAll('[data-field="' + e.field + '"][data-validator]'));
                messages.forEach((messageEle) => {
                    const validator = messageEle.getAttribute('data-validator');
                    messageEle.style.display = validator === e.validator ? 'block' : 'none';
                });
            }
        })
        .on('core.form.valid', function () {
            var parameters = new FormData(fv.form);
            parameters.append('action', 'upload_excel');
            submit_formdata_with_ajax('Alerta', '¿Estas seguro de guardar el siguiente archivo?', pathname, parameters, function () {
                alert_sweetalert('success', 'Alerta', 'Productos actualizados correctamente', function () {
                    location.reload();
                }, 2000, null);
            });
        });
});

$(function () {
    $('.btnUpload').on('click', function () {
        $('#myModalUploadExcel').modal('show');
    });
});