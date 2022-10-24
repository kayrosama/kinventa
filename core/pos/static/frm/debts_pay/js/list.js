var tblPaymentsDebtsPay, tblDebtsPay;
var date_current;
var input_date_range;
var debts_pay = {
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
        tblDebtsPay = $('#data').DataTable({
            autoWidth: false,
            destroy: true,
            ajax: {
                url: pathname,
                type: 'POST',
                headers: {
                    'X-CSRFToken': csrftoken
                },
                data: parameters,
                dataSrc: ""
            },
            columns: [
                {data: "purchase.number"},
                {data: "purchase.provider.name"},
                {data: "date_joined"},
                {data: "end_date"},
                {data: "debt"},
                {data: "saldo"},
                {data: "state"},
                {data: "state"},
            ],
            columnDefs: [
                {
                    targets: [-1],
                    orderable: false,
                    class: 'text-center',
                    render: function (data, type, row) {
                        var buttons = '<a rel="payments" class="btn bg-blue btn-xs btn-flat"><i class="fas fa-dollar-sign"></i></a> ';
                        buttons += '<a href="' + pathname + 'delete/' + row.id + '/" class="btn btn-danger btn-xs btn-flat"><i class="fas fa-trash"></i></a>';
                        return buttons;
                    }
                },
                {
                    targets: [-5, -6],
                    class: 'text-center',
                },
                {
                    targets: [-3, -4],
                    orderable: false,
                    class: 'text-center',
                    render: function (data, type, row) {
                        return '$' + data;
                    }
                },
                {
                    targets: [-2],
                    orderable: false,
                    class: 'text-center',
                    render: function (data, type, row) {
                        if (data) {
                            return '<span class="badge badge-danger badge-pill">Adeuda</span>';
                        }
                        return '<span class="badge badge-success badge-pill">Pagado</span>';
                    }
                }
            ],
            initComplete: function (settings, json) {
                $(this).wrap('<div class="dataTables_scroll"><div/>');
                var total = json.reduce((a, b) => a + (parseFloat(b.saldo) || 0), 0);
                $('.total').html('$' + total.toFixed(2));
            }
        });
    }
};

$(function () {

    input_date_range = $('input[name="date_range"]');

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
            debts_pay.list(false);
        });

    $('.drp-buttons').hide();

    debts_pay.list(false);

    $('.btnSearchAll').on('click', function () {
        debts_pay.list(true);
    });

    $('#data tbody')
        .off()
        .on('click', 'a[rel="payments"]', function () {
            $('.tooltip').remove();
            var tr = tblDebtsPay.cell($(this).closest('td, li')).index(),
                row = tblDebtsPay.row(tr.row).data();
            tblPaymentsDebtsPay = $('#tblPayments').DataTable({
                autoWidth: false,
                destroy: true,
                searching: false,
                ajax: {
                    url: pathname,
                    type: 'POST',
                    headers: {
                        'X-CSRFToken': csrftoken
                    },
                    data: function (d) {
                        d.action = 'search_pays';
                        d.id = row.id;
                    },
                    dataSrc: ""
                },
                columns: [
                    {data: "index"},
                    {data: "date_joined"},
                    {data: "valor"},
                    {data: "description"},
                    {data: "valor"},
                ],
                columnDefs: [
                    {
                        targets: [-3],
                        class: 'text-center',
                        render: function (data, type, row) {
                            return '$' + data;
                        }
                    },
                    {
                        targets: [-1],
                        class: 'text-center',
                        render: function (data, type, row) {
                            return '<a rel="delete" class="btn btn-danger btn-xs btn-flat"><i class="fas fa-times"></i></a>';
                        }
                    }
                ],
                rowCallback: function (row, data, index) {

                },
                initComplete: function (settings, json) {
                    $(this).wrap('<div class="dataTables_scroll"><div/>');
                }
            });
            $('#myModalPayments').modal('show');
        });

    $('#tblPayments tbody')
        .off()
        .on('click', 'a[rel="delete"]', function () {
            $('.tooltip').remove();
            var tr = tblPaymentsDebtsPay.cell($(this).closest('td, li')).index(),
                row = tblPaymentsDebtsPay.row(tr.row).data();
            submit_with_ajax('Notificación',
                '¿Estas seguro de eliminar el registro?',
                pathname,
                {
                    'id': row.id,
                    'action': 'delete_pay'
                },
                function () {
                    tblPaymentsDebtsPay.ajax.reload();
                }
            );
        });

    $('#myModalPayments').on('hidden.bs.modal', function () {
        tblDebtsPay.ajax.reload();
    });
});
