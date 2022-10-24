var product = {
    list: function () {
        var parameters = {
            'action': 'search',
        };
        $('#data').DataTable({
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
            columns: [
                {data: "id"},
                {data: "name"},
                {data: "code"},
                {data: "category.name"},
                {data: "inventoried"},
                {data: "image"},
                {data: "price"},
                {data: "pvp"},
                {data: "price_promotion"},
                {data: "stock"},
                {data: "id"},
            ],
            columnDefs: [
                {
                    targets: [-7],
                    class: 'text-center',
                    render: function (data, type, row) {
                        if (row.inventoried) {
                            return 'Si';
                        }
                        return 'No';
                    }
                },
                {
                    targets: [-6],
                    class: 'text-center',
                    render: function (data, type, row) {
                        return '<img alt="" src="' + row.image + '" class="img-fluid d-block mx-auto" style="width: 20px; height: 20px;">';
                    }
                },
                {
                    targets: [-4, -5, -3],
                    class: 'text-center',
                    render: function (data, type, row) {
                        return '$' + parseFloat(data).toFixed(2);
                    }
                },
                {
                    targets: [-2],
                    class: 'text-center',
                    render: function (data, type, row) {
                        if (row.inventoried) {
                            if (row.stock > 0) {
                                return '<span class="badge badge-success badge-pill">' + row.stock + '</span>';
                            }
                            return '<span class="badge badge-danger badge-pill">' + row.stock + '</span>';
                        }
                        return '<span class="badge badge-secondary badge-pill">Sin stock</span>';
                    }
                },
                {
                    targets: [-1],
                    class: 'text-center',
                    render: function (data, type, row) {
                        var buttons = '';
                        buttons += '<a href="' + pathname + 'update/' + row.id + '/" class="btn btn-warning btn-xs btn-flat"><i class="fas fa-edit"></i></a> ';
                        buttons += '<a href="' + pathname + 'delete/' + row.id + '/" class="btn btn-danger btn-xs btn-flat"><i class="fas fa-trash"></i></a> ';
                        return buttons;
                    }
                },
            ],
            rowCallback: function (row, data, index) {

            },
            initComplete: function (settings, json) {
                $(this).wrap('<div class="dataTables_scroll"><div/>');
            }
        });
    }
};

$(function () {
    product.list();

    $('#data').addClass('table-sm');
})