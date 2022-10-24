var tblDevolution;
var input_date_range;
var devolution = {
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
        tblDevolution = $('#data').DataTable({
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
                {data: "id"},
                {data: "sale_detail.sale.number"},
                {data: "sale_detail.product.name"},
                {data: "date_joined"},
                {data: "cant"},
                {data: "motive"},
                {data: "id"},
            ],
            columnDefs: [
                {
                    targets: [-1],
                    orderable: false,
                    class: 'text-center',
                    render: function (data, type, row) {
                        return '<a href="' + pathname + 'delete/' + row.id + '/" class="btn btn-danger btn-xs btn-flat"><i class="fas fa-trash"></i></a>';
                    }
                },
            ],
            initComplete: function (settings, json) {
                $(this).wrap('<div class="dataTables_scroll"><div/>');
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
            devolution.list(false);
        });

    $('.drp-buttons').hide();

    devolution.list(false);

    $('.btnSearchAll').on('click', function () {
        devolution.list(true);
    });
});
