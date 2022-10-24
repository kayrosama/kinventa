var fv;
var input_datejoined;
var select_debts_pay;

document.addEventListener('DOMContentLoaded', function (e) {
    fv = FormValidation.formValidation(document.getElementById('frmForm'), {
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
                debts_pay: {
                    validators: {
                        notEmpty: {
                            message: 'Seleccione un cuenta por pagar'
                        }
                    }
                },
                date_joined: {
                    validators: {
                        notEmpty: {
                            message: 'La fecha es obligatoria'
                        },
                        date: {
                            format: 'YYYY-MM-DD',
                            message: 'La fecha no es válida'
                        }
                    }
                },
                valor: {
                    validators: {
                        numeric: {
                            message: 'El valor no es un número',
                            thousandsSeparator: '',
                            decimalSeparator: '.'
                        }
                    }
                },
                description: {
                    validators: {}
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
            submit_formdata_with_ajax('Notificación',
                '¿Estas seguro de realizar la siguiente acción?',
                pathname,
                parameters,
                function () {
                    location.href = fv.form.getAttribute('data-url');
                }
            );
        });
});

$(function () {

    input_datejoined = $('input[name="date_joined"]');
    select_debts_pay = $('select[name="debts_pay"]');

    $('.select2').select2({
        theme: 'bootstrap4',
        language: "es"
    });

    select_debts_pay.select2({
        theme: "bootstrap4",
        language: 'es',
        allowClear: true,
        ajax: {
            delay: 250,
            type: 'POST',
            headers: {
                'X-CSRFToken': csrftoken
            },
            url: pathname,
            data: function (params) {
                return {
                    term: params.term,
                    action: 'search_debts_pay'
                };
            },
            processResults: function (data) {
                return {
                    results: data
                };
            },
        },
        placeholder: 'Ingrese el nombre del proveedor o número de factura',
        minimumInputLength: 1,
    })
        .on('select2:select', function (e) {
            fv.revalidateField('debts_pay');
            var data = e.params.data;
            $('.deuda').html('Deuda: $' + parseFloat(data.saldo).toFixed(2));
            $('input[name="valor"]').trigger("touchspin.updatesettings", {max: parseFloat(data.saldo)});
        })
        .on('select2:clear', function (e) {
            fv.revalidateField('debts_pay');
            $('.deuda').html('');
        });

    $('input[name="valor"]').TouchSpin({
        min: 0.01,
        max: 1000000,
        step: 0.01,
        decimals: 2,
        boostat: 5,
        maxboostedstep: 10,
        prefix: '$',
        verticalbuttons: true,
    }).on('change touchspin.on.min touchspin.on.max', function () {
        fv.revalidateField('valor');
    }).on('keypress', function (e) {
        return validate_decimals($(this), e);
    });

    input_datejoined.datetimepicker({
        format: 'YYYY-MM-DD',
        locale: 'es',
        keepOpen: false,
        // date: new moment().format("YYYY-MM-DD")
    });

    input_datejoined.on('change.datetimepicker', function () {
        fv.revalidateField('date_joined');
    });

    $('.deuda').html('');
});
