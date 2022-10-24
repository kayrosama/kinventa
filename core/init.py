from config.wsgi import *
import random
import string
from core.security.models import *
from django.contrib.auth.models import Permission
from core.pos.models import *

numbers = list(string.digits)

dashboard = Dashboard()
dashboard.name = 'Old Garage Garden'
dashboard.icon = 'fas fa-shopping-cart'
dashboard.layout = 1
dashboard.navbar = 'navbar-dark navbar-primary'
dashboard.sidebar = 'sidebar-dark-primary'
dashboard.save()

company = Company()
company.name = 'Old Garage Garden S. A.'
company.ruc = ''.join(random.choices(numbers, k=13))
company.email = 'kazuya.nishima@gmail.com'
company.phone = ''.join(random.choices(numbers, k=7))
company.mobile = ''.join(random.choices(numbers, k=10))
company.description = 'Ventas Al Por Mayor Y Por Menor En Productos para Taller.'
company.website = 'https://kayrosama.io'
company.address = '53 Calle Calzada Atanasio Tzul zona 21 Guatemala'
company.iva = 12.00
company.save()

moduletype = ModuleType()
moduletype.name = 'Seguridad'
moduletype.icon = 'fas fa-lock'
moduletype.save()
print(f'insertado {moduletype.name}')

module = Module()
module.module_type_id = 1
module.name = 'Tipos de Módulos'
module.url = '/security/module/type/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-door-open'
module.description = 'Permite administrar los tipos de módulos del sistema'
module.save()
for i in Permission.objects.filter(content_type__model=ModuleType._meta.label.split('.')[1].lower()):
    module.permits.add(i)
print(f'insertado {module.name}')

module = Module()
module.module_type_id = 1
module.name = 'Módulos'
module.url = '/security/module/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-th-large'
module.description = 'Permite administrar los módulos del sistema'
module.save()
for i in Permission.objects.filter(content_type__model=Module._meta.label.split('.')[1].lower()):
    module.permits.add(i)
print(f'insertado {module.name}')

module = Module()
module.module_type_id = 1
module.name = 'Grupos'
module.url = '/security/group/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-users'
module.description = 'Permite administrar los grupos de usuarios del sistema'
module.save()
for i in Permission.objects.filter(content_type__model=Group._meta.label.split('.')[1].lower()):
    module.permits.add(i)
print(f'insertado {module.name}')

module = Module()
module.module_type_id = 1
module.name = 'Respaldos'
module.url = '/security/database/backups/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-database'
module.description = 'Permite administrar los respaldos de base de datos'
module.save()
for i in Permission.objects.filter(content_type__model=DatabaseBackups._meta.label.split('.')[1].lower()):
    module.permits.add(i)
print(f'insertado {module.name}')

module = Module()
module.module_type_id = 1
module.name = 'Conf. Dashboard'
module.url = '/security/dashboard/update/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-tools'
module.description = 'Permite configurar los datos de la plantilla'
module.save()
print(f'insertado {module.name}')

module = Module()
module.module_type_id = 1
module.name = 'Accesos'
module.url = '/security/access/users/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-user-secret'
module.description = 'Permite administrar los accesos de los usuarios'
module.save()
for i in Permission.objects.filter(content_type__model=AccessUsers._meta.label.split('.')[1].lower()):
    module.permits.add(i)
print(f'insertado {module.name}')

module = Module()
module.module_type_id = 1
module.name = 'Usuarios'
module.url = '/user/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-user'
module.description = 'Permite administrar a los administradores del sistema'
module.save()
for i in Permission.objects.filter(content_type__model=User._meta.label.split('.')[1].lower()):
    module.permits.add(i)
print(f'insertado {module.name}')

moduletype = ModuleType()
moduletype.name = 'Bodega'
moduletype.icon = 'fas fa-boxes'
moduletype.save()
print(f'insertado {moduletype.name}')

module = Module()
module.module_type_id = 2
module.name = 'Proveedores'
module.url = '/pos/scm/provider/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-truck'
module.description = 'Permite administrar a los proveedores de las compras'
module.save()
for i in Permission.objects.filter(content_type__model=Provider._meta.label.split('.')[1].lower()):
    module.permits.add(i)
print(f'insertado {module.name}')

module = Module()
module.module_type_id = 2
module.name = 'Categorías'
module.url = '/pos/scm/category/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-truck-loading'
module.description = 'Permite administrar las categorías de los productos'
module.save()
for i in Permission.objects.filter(content_type__model=Category._meta.label.split('.')[1].lower()):
    module.permits.add(i)
print(f'insertado {module.name}')

module = Module()
module.module_type_id = 2
module.name = 'Productos'
module.url = '/pos/scm/product/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-box'
module.description = 'Permite administrar los productos del sistema'
module.save()
module.permits.add(Permission.objects.get(codename='view_product'))
module.permits.add(Permission.objects.get(codename='add_product'))
module.permits.add(Permission.objects.get(codename='change_product'))
module.permits.add(Permission.objects.get(codename='delete_product'))
print(f'insertado {module.name}')

module = Module()
module.module_type_id = 2
module.name = 'Compras'
module.url = '/pos/scm/purchase/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-dolly-flatbed'
module.description = 'Permite administrar las compras de los productos'
module.save()
for i in Permission.objects.filter(content_type__model=Purchase._meta.label.split('.')[1].lower()):
    module.permits.add(i)
print(f'insertado {module.name}')

module = Module()
module.module_type_id = 2
module.name = 'Ajuste de Stock'
module.url = '/pos/scm/product/stock/adjustment/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-sliders-h'
module.description = 'Permite administrar los ajustes de stock de productos'
module.save()
module.permits.add(Permission.objects.get(codename='adjust_product_stock'))
print(f'insertado {module.name}')

moduletype = ModuleType()
moduletype.name = 'Administrativo'
moduletype.icon = 'fas fa-hand-holding-usd'
moduletype.save()
print(f'insertado {module.name}')

module = Module()
module.module_type_id = 3
module.name = 'Tipos de Gastos'
module.url = '/pos/frm/type/expense/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-comments-dollar'
module.description = 'Permite administrar los tipos de gastos'
module.save()
for i in Permission.objects.filter(content_type__model=TypeExpense._meta.label.split('.')[1].lower()):
    module.permits.add(i)
print(f'insertado {module.name}')

module = Module()
module.module_type_id = 3
module.name = 'Gastos'
module.url = '/pos/frm/expenses/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-file-invoice-dollar'
module.description = 'Permite administrar los gastos de la compañia'
module.save()
for i in Permission.objects.filter(content_type__model=Expenses._meta.label.split('.')[1].lower()):
    module.permits.add(i)
print(f'insertado {module.name}')

module = Module()
module.module_type_id = 3
module.name = 'Cuentas por cobrar'
module.url = '/pos/frm/ctas/collect/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-funnel-dollar'
module.description = 'Permite administrar las cuentas por cobrar de los clientes'
module.save()
for i in Permission.objects.filter(content_type__model=CtasCollect._meta.label.split('.')[1].lower()):
    module.permits.add(i)
print(f'insertado {module.name}')

module = Module()
module.module_type_id = 3
module.name = 'Cuentas por pagar'
module.url = '/pos/frm/debts/pay/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-money-check-alt'
module.description = 'Permite administrar las cuentas por pagar de los proveedores'
module.save()
for i in Permission.objects.filter(content_type__model=DebtsPay._meta.label.split('.')[1].lower()):
    module.permits.add(i)
print(f'insertado {module.name}')

moduletype = ModuleType()
moduletype.name = 'Facturación'
moduletype.icon = 'fas fa-calculator'
moduletype.save()
print(f'insertado {moduletype.name}')

module = Module()
module.module_type_id = 4
module.name = 'Clientes'
module.url = '/pos/crm/client/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-user-friends'
module.description = 'Permite administrar los clientes del sistema'
module.save()
for i in Permission.objects.filter(content_type__model=Client._meta.label.split('.')[1].lower()):
    module.permits.add(i)
print(f'insertado {module.name}')

module = Module()
module.module_type_id = 4
module.name = 'Ventas'
module.url = '/pos/crm/sale/admin/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-shopping-cart'
module.description = 'Permite administrar las ventas de los productos'
module.save()
module.permits.add(Permission.objects.get(codename='view_sale'))
module.permits.add(Permission.objects.get(codename='add_sale'))
module.permits.add(Permission.objects.get(codename='delete_sale'))
print(f'insertado {module.name}')

module = Module()
module.name = 'Ventas'
module.url = '/pos/crm/sale/client/'
module.is_active = True
module.is_vertical = False
module.is_visible = True
module.icon = 'fas fa-shopping-cart'
module.description = 'Permite administrar las ventas de los productos'
module.save()
module.permits.add(Permission.objects.get(codename='view_sale_client'))
print(f'insertado {module.name}')

module = Module()
module.module_type_id = 4
module.name = 'Promociones'
module.url = '/pos/crm/promotions/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'far fa-calendar-check'
module.description = 'Permite administrar las promociones de los productos'
module.save()
for i in Permission.objects.filter(content_type__model=Promotions._meta.label.split('.')[1].lower()):
    module.permits.add(i)
print(f'insertado {module.name}')

module = Module()
module.module_type_id = 4
module.name = 'Devoluciones'
module.url = '/pos/crm/devolution/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-exchange-alt'
module.description = 'Permite administrar las devoluciones de los productos'
module.save()
for i in Permission.objects.filter(content_type__model=Devolution._meta.label.split('.')[1].lower()):
    module.permits.add(i)
print(f'insertado {module.name}')

moduletype = ModuleType()
moduletype.name = 'Reportes'
moduletype.icon = 'fas fa-chart-pie'
moduletype.save()
print(f'insertado {moduletype.name}')

module = Module()
module.module_type_id = 5
module.name = 'Ventas'
module.url = '/reports/sale/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-chart-bar'
module.description = 'Permite ver los reportes de las ventas'
module.save()
print(f'insertado {module.name}')

module = Module()
module.module_type_id = 5
module.name = 'Compras'
module.url = '/reports/purchase/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-chart-bar'
module.description = 'Permite ver los reportes de las compras'
module.save()
print(f'insertado {module.name}')

module = Module()
module.module_type_id = 5
module.name = 'Gastos'
module.url = '/reports/expenses/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-chart-bar'
module.description = 'Permite ver los reportes de los gastos'
module.save()
print(f'insertado {module.name}')

module = Module()
module.module_type_id = 5
module.name = 'Cuentas por Pagar'
module.url = '/reports/debts/pay/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-chart-bar'
module.description = 'Permite ver los reportes de las cuentas por pagar'
module.save()
print(f'insertado {module.name}')

module = Module()
module.module_type_id = 5
module.name = 'Cuentas por Cobrar'
module.url = '/reports/ctas/collect/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-chart-bar'
module.description = 'Permite ver los reportes de las cuentas por cobrar'
module.save()
print(f'insertado {module.name}')

module = Module()
module.module_type_id = 5
module.name = 'Resultados'
module.url = '/reports/results/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-chart-bar'
module.description = 'Permite ver los reportes de perdidas y ganancias'
module.save()
print(f'insertado {module.name}')

module = Module()
module.module_type_id = 5
module.name = 'Ganancias'
module.url = '/reports/earnings/'
module.is_active = True
module.is_vertical = True
module.is_visible = True
module.icon = 'fas fa-chart-bar'
module.description = 'Permite ver los reportes de las ganancias'
module.save()
print(f'insertado {module.name}')

module = Module()
module.name = 'Cambiar password'
module.url = '/user/update/password/'
module.is_active = True
module.is_vertical = False
module.is_visible = True
module.icon = 'fas fa-key'
module.description = 'Permite cambiar tu password de tu cuenta'
module.save()
print(f'insertado {module.name}')

module = Module()
module.name = 'Editar perfil'
module.url = '/user/update/profile/'
module.is_active = True
module.is_vertical = False
module.is_visible = True
module.icon = 'fas fa-user'
module.description = 'Permite cambiar la información de tu cuenta'
module.save()
print(f'insertado {module.name}')

module = Module()
module.name = 'Editar perfil'
module.url = '/pos/crm/client/update/profile/'
module.is_active = True
module.is_vertical = False
module.is_visible = True
module.icon = 'fas fa-user'
module.description = 'Permite cambiar la información de tu cuenta'
module.save()
print(f'insertado {module.name}')

module = Module()
module.name = 'Compañia'
module.url = '/pos/crm/company/update/'
module.is_active = True
module.is_vertical = False
module.is_visible = True
module.icon = 'fas fa-building'
module.description = 'Permite gestionar la información de la compañia'
module.save()
for i in Permission.objects.filter(content_type__model=Company._meta.label.split('.')[1].lower()):
    module.permits.add(i)
print(f'insertado {module.name}')

group = Group()
group.name = 'Administrador'
group.save()
print(f'insertado {group.name}')
for m in Module.objects.filter().exclude(url__in=['/pos/crm/client/update/profile/', '/pos/crm/sale/client/']):
    gm = GroupModule()
    gm.module = m
    gm.group = group
    gm.save()
    for p in m.permits.all():
        group.permissions.add(p)
        grouppermission = GroupPermission()
        grouppermission.module_id = m.id
        grouppermission.group_id = group.id
        grouppermission.permission_id = p.id
        grouppermission.save()

group = Group()
group.name = 'Cliente'
group.save()
print(f'insertado {group.name}')
for m in Module.objects.filter(url__in=['/pos/crm/client/update/profile/', '/pos/crm/sale/client/', '/user/update/password/']).exclude():
    gm = GroupModule()
    gm.module = m
    gm.group = group
    gm.save()
    for p in m.permits.all():
        group.permissions.add(p)
        grouppermission = GroupPermission()
        grouppermission.module_id = m.id
        grouppermission.group_id = group.id
        grouppermission.permission_id = p.id
        grouppermission.save()

user = User()
user.names = 'Kazuya Nishima'
user.username = 'admin'
user.dni = ''.join(random.choices(numbers, k=10))
user.email = 'kazuya.nishima@gmail.com'
user.is_active = True
user.is_superuser = True
user.is_staff = True
user.set_password('kinteki666')
user.save()
group = Group.objects.get(pk=1)
user.groups.add(group)
print(f'Bienvenido {user.names}')
