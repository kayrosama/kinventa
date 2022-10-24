var input_search_products;
var tblProducts;
var tblSearchProducts;

var inventory = {
    details: {
        products: []
    },
    addProduct: function (item) {
        this.details.products.push(item);
        this.listProducts();
    },
    listProducts: function () {
        tblProducts = $('#tblProducts').DataTable({
            autoWidth: false,
            destroy: true,
            data: this.details.products,
            ordering: false,
            lengthChange: false,
            searching: false,
            paginate: false,
            columns: [
                {data: "id"},
                {data: "code"},
                {data: "full_name"},
                {data: "stock"},
                {data: "newstock"},
            ],
            columnDefs: [
                {
                    targets: [-1],
                    class: 'text-center',
                    render: function (data, type, row) {
                        return '<input type="text" class="form-control" autocomplete="off" name="newstock" value="' + row.newstock + '">';
                    }
                },
                {
                    targets: [-2],
                    class: 'text-center',
                    render: function (data, type, row) {
                        return data;
                    }
                },
                {
                    targets: [0],
                    class: 'text-center',
                    render: function (data, type, row) {
                        return '<a rel="remove" class="btn btn-danger btn-flat btn-xs"><i class="fas fa-times"></i></a>';
                    }
                },
            ],
            rowCallback: function (row, data, index) {
                var tr = $(row).closest('tr');
                tr.find('input[name="newstock"]')
                    .TouchSpin({
                        min: 0,
                        max: 10000000,
                        verticalbuttons: true,
                    })
                    .on('keypress', function (e) {
                        return validate_form_text('numbers', e, null);
                    });
            },
            initComplete: function (settings, json) {

            },
        });
    },
    getProductsIds: function () {
        return  this.details.products.map(value => value.id);
    },
};

$(function () {

    input_search_products = $('input[name="input_search_products"]');

    input_search_products.autocomplete({
        source: function (request, response) {
            $.ajax({
                url: pathname,
                data: {
                    'action': 'search_products',
                    'term': request.term,
                    'ids': JSON.stringify(inventory.getProductsIds()),
                },
                dataType: "json",
                type: "POST",
                headers: {
                    'X-CSRFToken': csrftoken
                },
                beforeSend: function () {

                },
                success: function (data) {
                    response(data);
                }
            });
        },
        min_length: 3,
        delay: 300,
        select: function (event, ui) {
            event.preventDefault();
            $(this).blur();
            ui.item.newstock = ui.item.stock;
            inventory.addProduct(ui.item);
            $(this).val('').focus();
        }
    });

    $('.btnClearProducts').on('click', function () {
        input_search_products.val('').focus();
    });

    $('#tblProducts tbody')
        .off()
        .on('change', 'input[name="newstock"]', function () {
            var tr = tblProducts.cell($(this).closest('td, li')).index();
            inventory.details.products[tr.row].newstock = parseInt($(this).val());
        })
        .on('click', 'a[rel="remove"]', function () {
            var tr = tblProducts.cell($(this).closest('td, li')).index();
            inventory.details.products.splice(tr.row, 1);
            tblProducts.row(tr.row).remove().draw();
            $('.tooltip').remove();
        });

    $('.btnSearchProducts').on('click', function () {
        tblSearchProducts = $('#tblSearchProducts').DataTable({
            autoWidth: false,
            destroy: true,
            ajax: {
                url: pathname,
                type: 'POST',
                headers: {
                    'X-CSRFToken': csrftoken
                },
                data: {
                    'action': 'search_products',
                    'term': input_search_products.val(),
                    'ids': JSON.stringify(inventory.getProductsIds()),
                },
                dataSrc: ""
            },
            columns: [
                {data: "code"},
                {data: "full_name"},
                {data: "stock"},
                {data: "id"},
            ],
            columnDefs: [
                {
                    targets: [-2],
                    class: 'text-center',
                    render: function (data, type, row) {
                        if (row.stock > 0) {
                            return '<span class="badge badge-success badge-pill">' + data + '</span>'
                        }
                        return '<span class="badge badge-warning badge-pill">' + data + '</span>'
                    }
                },
                {
                    targets: [-1],
                    class: 'text-center',
                    render: function (data, type, row) {
                        return '<a rel="add" class="btn btn-success btn-flat btn-xs"><i class="fas fa-plus"></i></a>'
                    }
                }
            ],
            rowCallback: function (row, data, index) {
                var tr = $(row).closest('tr');
                if (data.stock === 0) {
                    $(tr).css({'background': '#dc3345', 'color': 'white'});
                }
            },
        });
        $('#myModalSearchProducts').modal('show');
    });

    $('#tblSearchProducts tbody')
        .off()
        .on('click', 'a[rel="add"]', function () {
            var tr = tblSearchProducts.cell($(this).closest('td, li')).index();
            var row = tblSearchProducts.row(tr.row).data();
            row.newstock = row.stock;
            inventory.addProduct(row);
            tblSearchProducts.row(tblSearchProducts.row(tr.row).node()).remove().draw();
        });

    $('.btnRemoveAllProducts').on('click', function () {
        if (inventory.details.products.length === 0) return false;
        dialog_action('Notificación', '¿Estas seguro de eliminar todos los items de tu detalle?', function () {
            inventory.details.products = [];
            inventory.listProducts();
        }, function () {

        });
    });

    inventory.listProducts();

    $('.btnSave').on('click', function () {
        if (inventory.details.products.length === 0) {
            message_error('Debe tener al menos un producto en su detalle');
            return false;
        }
        submit_with_ajax('Notificación', '¿Estas seguro de realizar la siguiente acción?', pathname,
            {
                'action': 'create',
                'products': JSON.stringify(inventory.details.products)
            },
            function (request) {
                location.href = $('.btnRefresh').attr('href');
            }
        );
    });

    $('i[data-field="input_search_products"]').hide();
})