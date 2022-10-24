var fv;
var input_datejoined;
var select_sale;
var tblProducts = null;

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
                sale: {
                    validators: {
                        notEmpty: {
                            message: 'Seleccione una venta'
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
            var parameters = new FormData(fv.form);
            var products = devolution.getProducts();
            if (products.length === 0) {
                message_error('Debe tener al menos un item seleccionado');
                return false;
            }
            parameters.append('products', JSON.stringify(products));
            submit_formdata_with_ajax('Notificación',
                '¿Estas seguro de realizar la siguiente acción?',
                pathname,
                parameters,
                function () {
                    location.href = fv.form.getAttribute('data-url');
                },
            );
        });
});

var devolution = {
    listDetailProducts: function () {
        var id = select_sale.val();
        if ($.isEmptyObject(id)) {
            if (tblProducts !== null) {
                tblProducts.clear().draw();
            }
            return false;
        }
        tblProducts = $('#tblProducts').DataTable({
            autoWidth: false,
            destroy: true,
            deferRender: true,
            paging: false,
            ordering: false,
            info: false,
            ajax: {
                url: pathname,
                type: 'POST',
                headers: {
                    'X-CSRFToken': csrftoken
                },
                data: {
                    'action': 'search_products_detail',
                    'id': id,
                },
                dataSrc: ""
            },
            columns: [
                {data: "id"},
                {data: "product.name"},
                {data: "cant"},
                {data: "amount_return"},
                {data: "motive"},
                {data: "state"},
            ],
            columnDefs: [
                {
                    targets: [-1],
                    class: 'text-center',
                    render: function (data, type, row) {
                        if (row.cant > 0) {
                            return '<input type="checkbox" class="form-control form-control-checkbox" name="state">';
                        }
                        return '---';
                    }
                },
                {
                    targets: [-2],
                    class: 'text-center',
                    render: function (data, type, row) {
                        if (row.cant > 0) {
                            return '<input type="text" class="form-control" name="motive" disabled placeholder="Ingrese una descripción" autocomplete="off">';
                        }
                        return '---';
                    }
                },
                {
                    targets: [-3],
                    class: 'text-center',
                    render: function (data, type, row) {
                        if (row.cant > 0) {
                            return '<input type="text" class="form-control" name="amount_return" disabled value="0">';
                        }
                        return '---';
                    }
                },
            ],
            rowCallback: function (row, data, index) {
                var tr = $(row).closest('tr');
                tr.find('input[name="amount_return"]')
                    .TouchSpin({
                        min: 1,
                        max: data.cant,
                        verticalbuttons: true,
                    })
                    .on('keypress', function (e) {
                        return validate_form_text('numbers', e, null);
                    });
            },
            initComplete: function (settings, json) {
                $(this).wrap('<div class="dataTables_scroll"><div/>');
            }
        });
    },
    getProducts: function () {
        return tblProducts.rows().data().toArray().filter(value => value.state === 1 && value.amount_return > 0);
    }
};

$(function () {

    input_datejoined = $('input[name="date_joined"]');
    select_sale = $('select[name="sale"]');

    $('.select2').select2({
        theme: 'bootstrap4',
        language: "es"
    });

    select_sale.select2({
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
                    action: 'search_sale'
                };
            },
            processResults: function (data) {
                return {
                    results: data
                };
            },
        },
        placeholder: 'Ingrese una descripción',
        minimumInputLength: 1,
    })
        .on('select2:select', function (e) {
            fv.revalidateField('sale');
            devolution.listDetailProducts();
        })
        .on('select2:clear', function (e) {
            fv.revalidateField('sale');
            devolution.listDetailProducts();
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

    $('#tblProducts tbody')
        .off()
        .on('change', 'input[name="amount_return"]', function () {
            var tr = tblProducts.cell($(this).closest('td, li')).index();
            var row = tblProducts.row(tr.row).data();
            row.amount_return = parseInt($(this).val());
        })
        .on('keyup', 'input[name="motive"]', function () {
            var tr = tblProducts.cell($(this).closest('td, li')).index();
            var row = tblProducts.row(tr.row).data();
            row.motive = $(this).val();
        })
        .on('change', 'input[name="state"]', function () {
            var state = this.checked;
            var tr = tblProducts.cell($(this).closest('td, li')).index();
            var row = tblProducts.row(tr.row).data();
            row.state = state ? 1 : 0;
            row.amount_return = state ? 1 : 0;
            $(tblProducts.row(tr.row).node()).find('input[name="amount_return"]').prop('disabled', !state);
            $(tblProducts.row(tr.row).node()).find('input[name="motive"]').prop('disabled', !state);
        });
});
