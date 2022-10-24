var tblPaymentsCtasCollect, tblCtasCollect;
var date_current;
var input_date_range;
var ctas_collect = {
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
        tblCtasCollect = $('#data').DataTable({
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
                {data: "sale.number"},
                {data: "sale.client"},
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
                    targets: [1],
                    class: 'text-center',
                    render: function (data, type, row) {
                        if (!$.isEmptyObject(row.sale.client)) {
                            return row.sale.client.user.names;
                        }
                        return 'Consumidor final';
                    }
                },
                {
                    targets: [-6, -7],
                    class: 'text-center',
                    render: function (data, type, row) {
                        return data;
                    }
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
            ctas_collect.list(false);
        });

    $('.drp-buttons').hide();

    ctas_collect.list(false);

    $('.btnSearchAll').on('click', function () {
        ctas_collect.list(true);
    });

    $('#data tbody')
        .off()
        .on('click', 'a[rel="payments"]', function () {
            $('.tooltip').remove();
            var tr = tblCtasCollect.cell($(this).closest('td, li')).index(),
                row = tblCtasCollect.row(tr.row).data();
            tblPaymentsCtasCollect = $('#tblPayments').DataTable({
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
            var tr = tblPaymentsCtasCollect.cell($(this).closest('td, li')).index(),
                row = tblPaymentsCtasCollect.row(tr.row).data();
            submit_with_ajax('Notificación',
                '¿Estas seguro de eliminar el registro?',
                pathname,
                {
                    'id': row.id,
                    'action': 'delete_pay'
                },
                function () {
                    tblPaymentsCtasCollect.ajax.reload();
                }
            );
        });

    $('#myModalPayments').on('hidden.bs.modal', function () {
        tblCtasCollect.ajax.reload();
    });
});
