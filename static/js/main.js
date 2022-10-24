var pathname = window.location.pathname;
var nav = $('body');

var page = {
    components: {
        vertical: {
            nav: 'sidebar-collapse',
            module_header: 'module_header',
            submodule: 'submodule',
            single_module: 'single_module',
        },
        horizontal: {
            module_header: 'module_header',
            single_module: 'single_module'
        }
    },
    initial: function () {
        console.log(localStorage);
        var element = null;
        // vertical
        if (localStorage.getItem(this.components.vertical.nav)) {
            nav.addClass(this.components.vertical.nav);
        }
        if (localStorage.getItem(this.components.vertical.module_header)) {
            element = nav.find('li.nav-item[data-name="module_header"][data-id="' + localStorage.getItem(this.components.vertical.module_header) + '"]')
            element.addClass('menu-is-opening menu-open');
            element.find('a.nav-link[data-name="module_header"]').addClass('active');
        }
        if (localStorage.getItem(this.components.vertical.submodule)) {
            element = nav.find('li.nav-item .nav-treeview a.nav-link[data-name="submodule"][data-id="' + localStorage.getItem(this.components.vertical.submodule) + '"]');
            element.addClass('active');
        }
        if (localStorage.getItem(this.components.vertical.single_module)) {
            element = nav.find('li.nav-item a.nav-link[data-name="single_module"][data-id="' + localStorage.getItem(this.components.vertical.single_module) + '"]');
            element.addClass('active');
        }
        // // horizontal
        if (localStorage.getItem(this.components.horizontal.module_header)) {
            element = $('.nav-tabs li.nav-item a[data-name="module_header"][href="' + localStorage.getItem(this.components.horizontal.module_header) + '"]');
            element.tab('show');
            var parent = element.closest('ul.nav-tabs').parent().find('.tab-content');
            if (localStorage.getItem(this.components.horizontal.single_module)) {
                var card = parent.find('.tab-pane[data-id="' + localStorage.getItem(this.components.horizontal.module_header) + '"] a.card-icon[data-id="' + localStorage.getItem(this.components.horizontal.single_module) + '"]');
                card.addClass('card-icon-selected');
            }
        }
    }
};

$(function () {

    $('[data-toggle="tooltip"]').tooltip();

    $('.table')
        .on('draw.dt', function () {
            $('[data-toggle="tooltip"]').tooltip();
        })
        .on('click', 'img', function () {
            var src = $(this).attr('src');
            load_image(src);
        });

    // Vertical

    $('nav .navbar-nav .collapsedMenu').on('click', function () {
        if (!nav.hasClass(page.components.vertical.nav)) {
            localStorage.setItem(page.components.vertical.nav, true);
        } else {
            localStorage.removeItem(page.components.vertical.nav);
        }
    });

    $('.sidebar li.nav-item')
        .on('click', 'a.nav-link[data-name="single_module"]', function () {
            var element = $(this);
            localStorage.removeItem(page.components.vertical.module_header);
            localStorage.removeItem(page.components.vertical.submodule);
            localStorage.setItem(page.components.vertical.single_module, element.data('id'));
        })
        .on('click', 'ul.nav-treeview a.nav-link[data-name="submodule"]', function () {
            var element = $(this);
            localStorage.setItem(page.components.vertical.submodule, element.data('id'));
        })
        .on('click', 'a.nav-link[data-name="module_header"]', function () {
            var element = $(this);
            var parent = element.parent();
            if (!parent.hasClass('menu-is-opening')) {
                element.addClass('active');
                localStorage.setItem(page.components.vertical.module_header, parent.data('id'));
                localStorage.removeItem(page.components.vertical.submodule);
                var children = parent.closest('.nav-sidebar').find('li.menu-is-opening');
                children.find('a.nav-link[data-name="module_header"]').removeClass('active');
                children.find('ul.nav-treeview').css({'display': 'none'});
                children.removeClass('menu-is-opening menu-open');
                parent.children('ul.nav-treeview').find('a.nav-link[data-name="submodule"]').removeClass('active');
            } else {
                element.removeClass('active');
                localStorage.removeItem(page.components.vertical.module_header);
            }
            localStorage.removeItem(page.components.vertical.single_module);
            nav.find('li.nav-item a.nav-link[data-name="single_module"]').removeClass('active');
        });

    // Horizontal

    $('.nav-tabs li.nav-item a[data-name="module_header"]').on('click', function () {
        var href = $(this).attr('href');
        localStorage.setItem(page.components.horizontal.module_header, href);
    });

    $('.tab-content .tab-pane a[data-name="single_module"]')
        .off()
        .on('mouseenter mouseleave', function () {
            $(this).closest('.tab-pane').find('a.card-icon-selected').removeClass('card-icon-selected');
        })
        .on('click', function () {
            localStorage.setItem(page.components.horizontal.single_module, $(this).data('id'));
        });

    // logout

    $('.btnLogout').on('click', function () {
        localStorage.clear();
    });

    page.initial();
});