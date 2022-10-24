var tblSale;
var input_date_range;
var sale = {
    list: function (all) {
        var parameters = {
            'action': 'search',
            'start_date': input_date_range.data('daterangepicker').startDate.format('YYYY-MM-DD'),
            'end_date': input_date_range.data('daterangepicker').endDate.format('YYYY-MM-DD'),
        };
        if (all) {
            parameters['start_date'] = '';
            parameters['end_date'] = '';
        }
        tblSale = $('#data').DataTable({
            autoWidth: false,
            destroy: true,
            deferRender: true,
            ajax: {
                url: pathname,
                type: 'POST',
                headers: {
                    'X-CSRFToken': csrftoken
                },
                data: parameters,
                dataSrc: ""
            },
            order: [[0, "desc"], [5, "desc"]],
            columns: [
                {data: "number"},
                {data: "client.user.names"},
                {data: "payment_condition.name"},
                {data: "payment_method.name"},
                {data: "type_voucher.name"},
                {data: "date_joined"},
                {data: "total"},
                {data: "id"},
            ],
            columnDefs: [
                {
                    targets: [-6],
                    class: 'text-center',
                    render: function (data, type, row) {
                        if (row.payment_condition.id === 'credito') {
                            return '<span class="badge badge-warning badge-pill">' + row.payment_condition.name + '</span>';
                        }
                        return '<span class="badge badge-success badge-pill">' + row.payment_condition.name + '</span>';
                    }
                },
                {
                    targets: [-3, -4, -5],
                    class: 'text-center',
                    render: function (data, type, row) {
                        return data;
                    }
                },
                {
                    targets: [-2],
                    class: 'text-center',
                    render: function (data, type, row) {
                        return '$' + parseFloat(data).toFixed(2);
                    }
                },
                {
                    targets: [-1],
                    class: 'text-center',
                    render: function (data, type, row) {
                        var buttons = '';
                        buttons += '<a class="btn btn-info btn-xs btn-flat" rel="detail"><i class="fas fa-folder-open"></i></a> ';
                        buttons += '<a href="' + pathname + 'print/invoice/' + row.id + '/" target="_blank" class="btn btn-primary btn-xs btn-flat"><i class="fas fa-print"></i></a> ';
                        return buttons;
                    }
                },
            ],
            rowCallback: function (row, data, index) {

            },
            initComplete: function (settings, json) {
                $(this).wrap('<div class="dataTables_scroll"><div/>');
                var total = json.reduce((a, b) => a + (parseFloat(b.total) || 0), 0);
                $('.total').html('$' + total.toFixed(2));
            }
        });
    }
};

$(function () {

    input_date_range = $('input[name="date_range"]');

    $('#data tbody')
        .off()
        .on('click', 'a[rel="detail"]', function () {
            $('.tooltip').remove();
            var tr = tblSale.cell($(this).closest('td, li')).index();
            var row = tblSale.row(tr.row).data();
            $('#tblProducts').DataTable({
                autoWidth: false,
                destroy: true,
                ajax: {
                    url: pathname,
                    type: 'POST',
                    headers: {
                        'X-CSRFToken': csrftoken
                    },
                    data: {
                        'action': 'search_detail_products',
                        'id': row.id
                    },
                    dataSrc: ""
                },
                columns: [
                    {data: "product.full_name"},
                    {data: "price"},
                    {data: "cant"},
                    {data: "subtotal"},
                    {data: "dscto"},
                    {data: "total_dscto"},
                    {data: "total"},
                ],
                columnDefs: [
                    {
                        targets: [-1, -2, -4, -6],
                        class: 'text-center',
                        render: function (data, type, row) {
                            return '$' + parseFloat(data).toFixed(2);
                        }
                    },
                    {
                        targets: [-3],
                        class: 'text-center',
                        render: function (data, type, row) {
                            return parseFloat(data).toFixed(2) + '%';
                        }
                    },
                    {
                        targets: [-5],
                        class: 'text-center',
                        render: function (data, type, row) {
                            return data;
                        }
                    }
                ],
                initComplete: function (settings, json) {
                    $(this).wrap('<div class="dataTables_scroll"><div/>');
                }
            });

            var invoice = [];
            invoice.push({'id': 'Cliente', 'name': row.client.user.names});
            invoice.push({'id': 'Forma de Pago', 'name': row.payment_condition.name});
            invoice.push({'id': 'Método de Pago', 'name': row.payment_method.name});
            invoice.push({'id': 'Subtotal', 'name': '$' + row.subtotal});
            invoice.push({'id': 'Iva', 'name': row.iva + ' %'});
            invoice.push({'id': 'Total Iva', 'name': '$' + row.total_iva});
            invoice.push({'id': 'Descuento', 'name': row.dscto + ' %'});
            invoice.push({'id': 'Total Descuento', 'name': '$' + row.total_dscto});
            invoice.push({'id': 'Total a pagar', 'name': '$' + row.total});
            if (row.payment_method.id === 'efectivo') {
                invoice.push({'id': 'Efectivo', 'name': '$' + row.cash});
                invoice.push({'id': 'Cambio', 'name': '$' + row.change});
            } else if (row.payment_method.id === 'tarjeta_debito_credito') {
                invoice.push({'id': 'Número de tarjeta', 'name': row.card_number});
                invoice.push({'id': 'Titular de tarjeta', 'name': row.titular});
                invoice.push({'id': 'Monto a debitar', 'name': '$' + row.amount_debited});
            } else if (row.payment_method.id === 'efectivo_tarjeta') {
                invoice.push({'id': 'Efectivo', 'name': '$' + row.cash});
                invoice.push({'id': 'Número de tarjeta', 'name': row.card_number});
                invoice.push({'id': 'Titular de tarjeta', 'name': row.titular});
                invoice.push({'id': 'Monto a debitar', 'name': '$' + row.amount_debited});
            }

            $('#tblInvoice').DataTable({
                autoWidth: false,
                destroy: true,
                data: invoice,
                paging: false,
                ordering: false,
                info: false,
                columns: [
                    {data: "id"},
                    {data: "name"},
                ],
                columnDefs: [
                    {
                        targets: [0, 1],
                        class: 'text-left',
                        render: function (data, type, row) {
                            return data;
                        }
                    },
                ],
                initComplete: function (settings, json) {
                    $(this).wrap('<div class="dataTables_scroll"><div/>');
                }
            });

            $('.nav-tabs a[href="#home"]').tab('show');

            $('#myModalDetails').modal('show');
        })

    input_date_range
        .daterangepicker({
                language: 'auto',
                startDate: new Date(),
                locale: {
                    format: 'YYYY-MM-DD',
                },
                autoApply: true,
            }
        )
        .on('apply.daterangepicker', function (ev, picker) {
            sale.list(false);
        });

    $('.drp-buttons').hide();

    sale.list(false);

    $('.btnSearchAll').on('click', function () {
        sale.list(true);
    });
});
