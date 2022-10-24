var tblModules;
var group = {
    details: {
        modules: [],
    },
    list: function () {
        tblModules = $('#tblModules').DataTable({
            autoWidth: false,
            destroy: true,
            data: this.details.modules,
            lengthChange: false,
            paging: false,
            scrollX: true,
            scrollCollapse: true,
            columns: [
                {data: "id"},
                {data: "name"},
                {data: "name"},
                {data: "state"},
                {data: "permits"},
            ],
            columnDefs: [
                {
                    targets: [-3],
                    orderable: false,
                    render: function (data, type, row) {
                        if (!$.isEmptyObject(row.module_type)) {
                            return row.module_type.name;
                        }
                        return 'Ninguno';
                    }
                },
                {
                    targets: [-2],
                    orderable: false,
                    class: 'text-center',
                    render: function (data, type, row) {
                        var state = row.state === 1 ? " checked" : "";
                        var content = '<div class="checkbox">';
                        content += '<label><input type="checkbox" name="module"' + state + '></label>';
                        content += '</div>';
                        return content;
                    }
                },
                {
                    targets: [-1],
                    orderable: false,
                    render: function (data, type, row) {
                        var content = "";
                        row.permits.forEach(function (value, index, array) {
                            var state = value.state === 1 ? " checked" : "";
                            content += '<div class="form-check form-check-inline">';
                            content += '<input class="form-check-input" type="checkbox" data-position="' + index + '" name="permit"' + state + '>';
                            content += '<label class="form-check-label">' + value.codename + '</label>';
                            content += '</div>';
                        })
                        return content;
                    }
                },
            ],
            order: [[0, 'asc']],
            rowCallback: function (row, data, index) {
                if (data.state === 0) {
                    var tr = $(row).closest('tr');
                    tr.find('input[name="permit"]').prop('disabled', true);
                }
            },
            initComplete: function (settings, json) {
                $(this).wrap('<div class="dataTables_scroll"><div/>');
            }
        });
    },
    getPermits: function () {
        let modules = tblModules.rows().data().toArray();
        let data = [];
        modules.filter(value => value.state === 1).forEach(function (value, key) {
            value.permissions = [];
            if (!$.isEmptyObject(value.permits)) {
                value.permissions = value.permits.filter(value => value.state === 1);
            }
            data.push(value);
        });
        return data;
    }
};

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
                name: {
                    validators: {
                        notEmpty: {},
                        stringLength: {
                            min: 2,
                        },
                        remote: {
                            url: pathname,
                            data: function () {
                                return {
                                    parameter: fv.form.querySelector('[name="name"]').value,
                                    pattern: 'name',
                                    action: 'validate_data'
                                };
                            },
                            message: 'El nombre ya se encuentra registrado',
                            method: 'POST',
                            headers: {
                                'X-CSRFToken': csrftoken
                            },
                        }
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
            parameters.delete('module');
            parameters.delete('permit');
            parameters.append('groups_json', JSON.stringify(group.getPermits()));
            submit_formdata_with_ajax('Notificación',
                '¿Estas seguro de realizar la siguiente acción?',
                pathname,
                parameters,
                function () {
                    location.href = fv.form.getAttribute('data-url');
                }
            )
        });
});

$(function () {

    $('#tblModules tbody')
        .off()
        .on('change', 'input[name="module"]', function () {
            var tr = tblModules.cell($(this).closest('td, li')).index(),
                row = tblModules.row(tr.row).data();
            row.state = this.checked ? 1 : 0;
            if (!$.isEmptyObject(row.permits)) {
                $(tblModules.row(tr.row).node())
                    .find('input[name="permit"]')
                    .prop('disabled', !this.checked)
                    .prop('checked', this.checked).trigger('change');
            }
        })
        .on('change', 'input[name="permit"]', function () {
            var index = parseInt($(this).data('position'));
            var tr = tblModules.cell($(this).closest('td, li')).index(),
                row = tblModules.row(tr.row).data();
            row.permits[index].state = this.checked ? 1 : 0;
        });

    $('input[name="selectall"]')
        .on('change', function () {
            var state = this.checked;
            var cells = tblModules.cells().nodes();
            $(cells).find('input[name="module"]').prop('checked', state).trigger('change');
        });
});





