var fv;
var input_isvertical, input_action;
var select_module_type;

document.addEventListener('DOMContentLoaded', function (e) {
    fv = FormValidation.formValidation(document.getElementById('frmForm'), {
            locale: 'es_ES',
            localization: FormValidation.locales.es_ES,
            plugins: {
                trigger: new FormValidation.plugins.Trigger(),
                submitButton: new FormValidation.plugins.SubmitButton(),
                bootstrap: new FormValidation.plugins.Bootstrap(),
                excluded: new FormValidation.plugins.Excluded(),
                icon: new FormValidation.plugins.Icon({
                    valid: 'fa fa-check',
                    invalid: 'fa fa-times',
                    validating: 'fa fa-refresh',
                }),
            },
            fields: {
                url: {
                    validators: {
                        notEmpty: {},
                        stringLength: {
                            min: 2,
                        },
                        remote: {
                            url: pathname,
                            data: function () {
                                return {
                                    parameter: fv.form.querySelector('[name="url"]').value,
                                    pattern: 'url',
                                    action: 'validate_data'
                                };
                            },
                            message: 'La dirección url ya se encuentra registrada',
                            method: 'POST',
                            headers: {
                                'X-CSRFToken': csrftoken
                            },
                        }
                    }
                },
                name: {
                    validators: {
                        notEmpty: {},
                        stringLength: {
                            min: 2,
                        },
                    }
                },
                icon: {
                    validators: {}
                },
                description: {
                    validators: {}
                },
                image: {
                    validators: {
                        file: {
                            extension: 'jpeg,jpg,png',
                            type: 'image/jpeg,image/png',
                            maxFiles: 1,
                            message: 'Introduce una imagen válida'
                        }
                    }
                },
                module_type: {
                    validators: {
                        notEmpty: {},
                    }
                },
                permits: {
                    validators: {
                        //notEmpty: {},
                    }
                }
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
            submit_formdata_with_ajax_form(fv);
        });
});

$(function () {

    input_isvertical = $('input[name="is_vertical"]');
    input_action = $('input[name="action"]');
    select_module_type = $('select[name="module_type"]');

    $('.select2').select2({
        theme: 'bootstrap4',
        language: "es"
    });

    $('select[name="permits"]').select2({
        theme: 'bootstrap4',
        language: "es",
        placeholder: 'Buscar..',
    });

    input_isvertical.on('change', function () {
        var checked = this.checked;
        select_module_type.prop('disabled', !checked);
        if (!checked) {
            fv.disableValidator('module_type');
            select_module_type.val('').trigger('change');
        } else {
            fv.enableValidator('module_type');
        }
    });

    select_module_type.on('change.select2', function () {
        fv.revalidateField('module_type');
    });

    if (input_isvertical.is(':checked')) {
        input_isvertical.trigger('change');
    }
});







