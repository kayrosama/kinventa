var module = {
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
                {data: "module_type"},
                {data: "icon"},
                {data: "image"},
                {data: "is_vertical"},
                {data: "is_visible"},
                {data: "is_active"},
                {data: "id"},
            ],
            columnDefs: [
                {
                    targets: [2],
                    class: 'text-center',
                    render: function (data, type, row) {
                        if (!$.isEmptyObject(row.module_type)) {
                            return row.module_type.name;
                        }
                        return 'Ninguno';
                    }
                },
                {
                    targets: [-2, -3, -4],
                    class: 'text-center',
                    render: function (data, type, row) {
                        if (data) {
                            return '<span class="badge badge-success badge-pill">Activo</span>';
                        }
                        return '<span class="badge badge-danger badge-pill">Inactivo</span>';
                    }
                },
                {
                    targets: [-5],
                    class: 'text-center',
                    render: function (data, type, row) {
                        return '<img alt="" src="' + row.image + '" class="img-fluid mx-auto d-block" style="width: 20px; height: 20px;">';
                    }
                },
                {
                    targets: [-6],
                    class: 'text-center',
                    render: function (data, type, row) {
                        return '<i class="' + row.icon + '"></i>';
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
    module.list();
});