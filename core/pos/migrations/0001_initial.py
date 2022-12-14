# Generated by Django 4.0.2 on 2022-10-23 05:18

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True, verbose_name='Nombre')),
            ],
            options={
                'verbose_name': 'Categoria',
                'verbose_name_plural': 'Categorias',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mobile', models.CharField(max_length=10, unique=True, verbose_name='Teléfono')),
                ('birthdate', models.DateField(default=datetime.datetime.now, verbose_name='Fecha de nacimiento')),
                ('address', models.CharField(blank=True, max_length=500, null=True, verbose_name='Dirección')),
            ],
            options={
                'verbose_name': 'Cliente',
                'verbose_name_plural': 'Clientes',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Nombre')),
                ('ruc', models.CharField(max_length=20, verbose_name='Ruc')),
                ('address', models.CharField(max_length=200, verbose_name='Dirección')),
                ('mobile', models.CharField(max_length=15, verbose_name='Teléfono celular')),
                ('phone', models.CharField(max_length=15, verbose_name='Teléfono convencional')),
                ('email', models.CharField(max_length=50, verbose_name='Email')),
                ('website', models.CharField(max_length=250, verbose_name='Página web')),
                ('description', models.CharField(blank=True, max_length=500, null=True, verbose_name='Descripción')),
                ('image', models.ImageField(blank=True, null=True, upload_to='company/%Y/%m/%d', verbose_name='Logo')),
                ('iva', models.DecimalField(decimal_places=2, default=0.0, max_digits=10, verbose_name='Iva')),
            ],
            options={
                'verbose_name': 'Empresa',
                'verbose_name_plural': 'Empresas',
                'ordering': ['-id'],
                'permissions': (('view_company', 'Can view Empresa'),),
                'default_permissions': (),
            },
        ),
        migrations.CreateModel(
            name='CtasCollect',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_joined', models.DateField(default=datetime.datetime.now)),
                ('end_date', models.DateField(default=datetime.datetime.now)),
                ('debt', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('saldo', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('state', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'Cuenta por cobrar',
                'verbose_name_plural': 'Cuentas por cobrar',
                'ordering': ['-id'],
                'permissions': (('view_ctas_collect', 'Can view Cuenta por cobrar'), ('add_ctas_collect', 'Can add Cuenta por cobrar'), ('delete_ctas_collect', 'Can delete Cuenta por cobrar')),
                'default_permissions': (),
            },
        ),
        migrations.CreateModel(
            name='DebtsPay',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_joined', models.DateField(default=datetime.datetime.now)),
                ('end_date', models.DateField(default=datetime.datetime.now)),
                ('debt', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('saldo', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('state', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'Cuenta por pagar',
                'verbose_name_plural': 'Cuentas por pagar',
                'ordering': ['-id'],
                'permissions': (('view_debts_pay', 'Can view Cuenta por pagar'), ('add_debts_pay', 'Can add Cuenta por pagar'), ('delete_debts_pay', 'Can delete Cuenta por pagar')),
                'default_permissions': (),
            },
        ),
        migrations.CreateModel(
            name='Devolution',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_joined', models.DateField(default=datetime.datetime.now, verbose_name='Fecha de registro')),
                ('cant', models.IntegerField(default=0)),
                ('motive', models.CharField(blank=True, max_length=500, null=True)),
            ],
            options={
                'verbose_name': 'Devolución',
                'verbose_name_plural': 'Devoluciones',
                'ordering': ['-id'],
                'permissions': (('view_devolution', 'Can view Devolución'), ('add_devolution', 'Can add Devolución'), ('delete_devolution', 'Can delete Devolución')),
                'default_permissions': (),
            },
        ),
        migrations.CreateModel(
            name='Expenses',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(blank=True, max_length=500, null=True, verbose_name='Descripción')),
                ('date_joined', models.DateField(default=datetime.datetime.now, verbose_name='Fecha de Registro')),
                ('valor', models.DecimalField(decimal_places=2, default=0.0, max_digits=10, verbose_name='Valor')),
            ],
            options={
                'verbose_name': 'Gasto',
                'verbose_name_plural': 'Gastos',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='PaymentsCtaCollect',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_joined', models.DateField(default=datetime.datetime.now, verbose_name='Fecha de registro')),
                ('description', models.CharField(blank=True, max_length=500, null=True, verbose_name='Detalles')),
                ('valor', models.DecimalField(decimal_places=2, default=0.0, max_digits=10, verbose_name='Valor')),
            ],
            options={
                'verbose_name': 'Pago Cuenta por cobrar',
                'verbose_name_plural': 'Pagos Cuentas por cobrar',
                'ordering': ['-id'],
                'default_permissions': (),
            },
        ),
        migrations.CreateModel(
            name='PaymentsDebtsPay',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_joined', models.DateField(default=datetime.datetime.now, verbose_name='Fecha de registro')),
                ('description', models.CharField(blank=True, max_length=500, null=True, verbose_name='Detalles')),
                ('valor', models.DecimalField(decimal_places=2, default=0.0, max_digits=10, verbose_name='Valor')),
            ],
            options={
                'verbose_name': 'Det. Cuenta por pagar',
                'verbose_name_plural': 'Det. Cuentas por pagar',
                'ordering': ['-id'],
                'default_permissions': (),
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='Nombre')),
                ('code', models.CharField(max_length=20, unique=True, verbose_name='Código')),
                ('description', models.CharField(blank=True, max_length=500, null=True, verbose_name='Descripción')),
                ('price', models.DecimalField(decimal_places=2, default=0.0, max_digits=10, verbose_name='Precio de Compra')),
                ('pvp', models.DecimalField(decimal_places=2, default=0.0, max_digits=10, verbose_name='Precio de Venta')),
                ('image', models.ImageField(blank=True, null=True, upload_to='product/%Y/%m/%d', verbose_name='Imagen')),
                ('inventoried', models.BooleanField(default=True, verbose_name='¿Es inventariado?')),
                ('stock', models.IntegerField(default=0)),
            ],
            options={
                'verbose_name': 'Producto',
                'verbose_name_plural': 'Productos',
                'ordering': ['-name'],
                'permissions': (('view_product', 'Can view Producto'), ('add_product', 'Can add Producto'), ('change_product', 'Can change Producto'), ('delete_product', 'Can delete Producto'), ('adjust_product_stock', 'Can adjust_product_stock Producto')),
                'default_permissions': (),
            },
        ),
        migrations.CreateModel(
            name='Promotions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField(default=datetime.datetime.now)),
                ('end_date', models.DateField(default=datetime.datetime.now)),
                ('state', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'Promoción',
                'verbose_name_plural': 'Promociones',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='PromotionsDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price_current', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('dscto', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('total_dscto', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('price_final', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
            ],
            options={
                'verbose_name': 'Detalle Promoción',
                'verbose_name_plural': 'Detalle de Promociones',
                'ordering': ['-id'],
                'default_permissions': (),
            },
        ),
        migrations.CreateModel(
            name='Provider',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True, verbose_name='Nombre')),
                ('ruc', models.CharField(max_length=20, unique=True, verbose_name='Ruc')),
                ('mobile', models.CharField(max_length=15, unique=True, verbose_name='Teléfono celular')),
                ('address', models.CharField(blank=True, max_length=500, null=True, verbose_name='Dirección')),
                ('email', models.CharField(max_length=50, unique=True, verbose_name='Email')),
            ],
            options={
                'verbose_name': 'Proveedor',
                'verbose_name_plural': 'Proveedores',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='Purchase',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(max_length=8, unique=True, verbose_name='Número de factura')),
                ('payment_condition', models.CharField(choices=[('contado', 'Contado'), ('credito', 'Credito')], default='contado', max_length=50, verbose_name='Condición de pago')),
                ('date_joined', models.DateField(default=datetime.datetime.now, verbose_name='Fecha de registro')),
                ('end_credit', models.DateField(default=datetime.datetime.now, verbose_name='Fecha de plazo de credito')),
                ('subtotal', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
            ],
            options={
                'verbose_name': 'Compra',
                'verbose_name_plural': 'Compras',
                'ordering': ['-id'],
                'permissions': (('view_purchase', 'Can view Compra'), ('add_purchase', 'Can add Compra'), ('delete_purchase', 'Can delete Compra')),
                'default_permissions': (),
            },
        ),
        migrations.CreateModel(
            name='PurchaseDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cant', models.IntegerField(default=0)),
                ('price', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('dscto', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('subtotal', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
            ],
            options={
                'verbose_name': 'Detalle de Compra',
                'verbose_name_plural': 'Detalle de Compras',
                'ordering': ['-id'],
                'default_permissions': (),
            },
        ),
        migrations.CreateModel(
            name='Sale',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_condition', models.CharField(choices=[('contado', 'Contado'), ('credito', 'Credito')], default='contado', max_length=50, verbose_name='Condición de pago')),
                ('payment_method', models.CharField(choices=[('efectivo', 'Efectivo'), ('tarjeta_debito_credito', 'Tarjeta de Debito / Credito'), ('efectivo_tarjeta', 'Efectivo y Tarjeta')], default='efectivo', max_length=50, verbose_name='Método de pago')),
                ('type_voucher', models.CharField(choices=[('ticket', 'Ticket'), ('factura', 'Factura')], default='ticket', max_length=50, verbose_name='Comprobante')),
                ('date_joined', models.DateField(default=datetime.datetime.now, verbose_name='Fecha de registro')),
                ('end_credit', models.DateField(default=datetime.datetime.now, verbose_name='Fecha limite de credito')),
                ('subtotal', models.DecimalField(decimal_places=2, default=0.0, max_digits=10, verbose_name='Subtotal')),
                ('dscto', models.DecimalField(decimal_places=2, default=0.0, max_digits=10, verbose_name='Descuento')),
                ('total_dscto', models.DecimalField(decimal_places=2, default=0.0, max_digits=10, verbose_name='Valor del descuento')),
                ('iva', models.DecimalField(decimal_places=2, default=0.0, max_digits=10, verbose_name='Iva')),
                ('total_iva', models.DecimalField(decimal_places=2, default=0.0, max_digits=10, verbose_name='Valor de iva')),
                ('total', models.DecimalField(decimal_places=2, default=0.0, max_digits=10, verbose_name='Total a pagar')),
                ('cash', models.DecimalField(decimal_places=2, default=0.0, max_digits=10, verbose_name='Efectivo recibido')),
                ('change', models.DecimalField(decimal_places=2, default=0.0, max_digits=10, verbose_name='Cambio')),
                ('card_number', models.CharField(blank=True, max_length=30, null=True, verbose_name='Número de tarjeta')),
                ('titular', models.CharField(blank=True, max_length=30, null=True, verbose_name='Titular')),
                ('amount_debited', models.DecimalField(decimal_places=2, default=0.0, max_digits=10, verbose_name='Monto a debitar')),
                ('client', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='pos.client', verbose_name='Cliente')),
            ],
            options={
                'verbose_name': 'Venta',
                'verbose_name_plural': 'Ventas',
                'ordering': ['-id'],
                'permissions': (('view_sale', 'Can view Venta'), ('add_sale', 'Can add Venta'), ('delete_sale', 'Can delete Venta'), ('view_sale_client', 'Can view_sale_client Venta')),
                'default_permissions': (),
            },
        ),
        migrations.CreateModel(
            name='TypeExpense',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True, verbose_name='Nombre')),
            ],
            options={
                'verbose_name': 'Tipo de Gasto',
                'verbose_name_plural': 'Tipos de Gastos',
                'ordering': ['id'],
                'permissions': (('view_type_expense', 'Can view Tipo de Gasto'), ('add_type_expense', 'Can add Tipo de Gasto'), ('change_type_expense', 'Can change Tipo de Gasto'), ('delete_type_expense', 'Can delete Tipo de Gasto')),
                'default_permissions': (),
            },
        ),
        migrations.CreateModel(
            name='SaleDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cant', models.IntegerField(default=0)),
                ('price', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('subtotal', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('dscto', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('total_dscto', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('total', models.DecimalField(decimal_places=2, default=0.0, max_digits=10)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='pos.product')),
                ('sale', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='pos.sale')),
            ],
            options={
                'verbose_name': 'Detalle de Venta',
                'verbose_name_plural': 'Detalle de Ventas',
                'ordering': ['-id'],
                'default_permissions': (),
            },
        ),
    ]
