var tblGroups;
var group = {
    list: function () {
        var parameters = {
            'action': 'search',
        };
        tblGroups = $('#data').DataTable({
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
                {data: "id"},
            ],
            columnDefs: [
                {
                    targets: [-1],
                    class: 'text-center',
                    render: function (data, type, row) {
                        var buttons = '<a rel="search" class="btn btn-success btn-xs btn-flat"><i class="fas fa-search"></i></a> ';
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

    group.list();

    $('#data tbody')
        .off()
        .on('click', 'a[rel="search"]', function () {
            $('.tooltip').remove();
            var tr = tblGroups.cell($(this).closest('td, li')).index(),
                row = tblGroups.row(tr.row).data();
            $('#tblModules').DataTable({
                autoWidth: false,
                destroy: true,
                ajax: {
                    url: pathname,
                    type: 'POST',
                    headers: {
                        'X-CSRFToken': csrftoken
                    },
                    data: {
                        'action': 'search_modules',
                        'id': row.id,
                    },
                    dataSrc: ""
                },
                columns: [
                    {"data": "name"},
                    {"data": "icon"},
                    {"data": "image"},
                    {"data": "module_type"},
                    {"data": "is_vertical"},
                    {"data": "is_visible"},
                    {"data": "is_active"},
                ],
                columnDefs: [
                    {
                        targets: [2],
                        class: 'text-center',
                        orderable: false,
                        render: function (data, type, row) {
                            return '<img class="img-fluid mx-auto d-block" src="' + data + '" width="20px" height="20px">';
                        }
                    },
                    {
                        targets: [3],
                        class: 'text-center',
                        render: function (data, type, row) {
                            if (!$.isEmptyObject(row.module_type)) {
                                return row.module_type.name;
                            }
                            return 'Ninguno';
                        }
                    },
                    {
                        targets: [1],
                        class: 'text-center',
                        orderable: false,
                        render: function (data, type, row) {
                            return '<i class="' + data + '" aria-hidden="true"></i>';
                        }
                    },
                    {
                        targets: [4, 5, 6],
                        class: 'text-center',
                        orderable: false,
                        data: null,
                        render: function (data, type, row) {
                            if (data) {
                                return '<i class="fa fa-check" aria-hidden="true"></i>';
                            }
                            return '<i class="fa fa-times" aria-hidden="true"></i>';
                        }
                    },
                ],
                initComplete: function (settings, json) {
                    $(this).wrap('<div class="dataTables_scroll"><div/>');
                }
            });
            $('#tblPermissions').DataTable({
                autoWidth: false,
                destroy: true,
                ajax: {
                    url: pathname,
                    type: 'POST',
                    headers: {
                        'X-CSRFToken': csrftoken
                    },
                    data: {
                        'action': 'search_permissions',
                        'id': row.id
                    },
                    dataSrc: ""
                },
                columns: [
                    {"data": "id"},
                    {"data": "name"},
                    {"data": "codename"},
                ],
                initComplete: function (settings, json) {
                    $(this).wrap('<div class="dataTables_scroll"><div/>');
                }
            });
            $('.nav-tabs a[href="#home"]').tab('show');
            $('#myModalGroup').modal('show');
        });
});