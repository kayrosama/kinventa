import math
import os
import re
from datetime import datetime

from django.db import models
from django.db.models import FloatField
from django.db.models import Sum
from django.db.models.functions import Coalesce
from django.forms import model_to_dict

from config import settings
from core.pos.choices import *
from core.user.models import User


class Company(models.Model):
    name = models.CharField(max_length=50, verbose_name='Nombre')
    ruc = models.CharField(max_length=20, verbose_name='Ruc')
    address = models.CharField(max_length=200, verbose_name='Dirección')
    mobile = models.CharField(max_length=15, verbose_name='Teléfono celular')
    phone = models.CharField(max_length=15, verbose_name='Teléfono convencional')
    email = models.CharField(max_length=50, verbose_name='Email')
    website = models.CharField(max_length=250, verbose_name='Página web')
    description = models.CharField(max_length=500, null=True, blank=True, verbose_name='Descripción')
    image = models.ImageField(null=True, blank=True, upload_to='company/%Y/%m/%d', verbose_name='Logo')
    iva = models.DecimalField(default=0.00, decimal_places=2, max_digits=10, verbose_name='Iva')

    def __str__(self):
        return self.name

    def get_image(self):
        if self.image:
            return f'{settings.MEDIA_URL}{self.image}'
        return f'{settings.STATIC_URL}img/default/empty.png'

    def get_iva(self):
        return f'{self.iva:.2f}'

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'Empresa'
        verbose_name_plural = 'Empresas'
        default_permissions = ()
        permissions = (
            ('view_company', 'Can view Empresa'),
        )
        ordering = ['-id']


class Provider(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name='Nombre')
    ruc = models.CharField(max_length=20, unique=True, verbose_name='Ruc')
    mobile = models.CharField(max_length=15, unique=True, verbose_name='Teléfono celular')
    address = models.CharField(max_length=500, null=True, blank=True, verbose_name='Dirección')
    email = models.CharField(max_length=50, unique=True, verbose_name='Email')

    def __str__(self):
        return self.get_full_name()

    def get_full_name(self):
        return f'{self.name} ({self.ruc})'

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'Proveedor'
        verbose_name_plural = 'Proveedores'
        ordering = ['-id']


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name='Nombre')

    def __str__(self):
        return self.name

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'
        ordering = ['-id']


class Product(models.Model):
    name = models.CharField(max_length=150, verbose_name='Nombre')
    code = models.CharField(max_length=20, unique=True, verbose_name='Código')
    description = models.CharField(max_length=500, null=True, blank=True, verbose_name='Descripción')
    category = models.ForeignKey(Category, on_delete=models.PROTECT, verbose_name='Categoría')
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name='Precio de Compra')
    pvp = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name='Precio de Venta')
    image = models.ImageField(upload_to='product/%Y/%m/%d', null=True, blank=True, verbose_name='Imagen')
    inventoried = models.BooleanField(default=True, verbose_name='¿Es inventariado?')
    stock = models.IntegerField(default=0)

    def __str__(self):
        return self.get_full_name()

    def get_full_name(self):
        return f'{self.name} ({self.code}) ({self.category.name})'

    def get_short_name(self):
        return f'{self.name} ({self.category.name})'

    def get_or_create_category(self, name):
        category = Category()
        search = Category.objects.filter(name=name)
        if search.exists():
            category = search[0]
        else:
            category.name = name
            category.save()
        return category

    def get_inventoried(self):
        if self.inventoried:
            return 'Inventariado'
        return 'No inventariado'

    def toJSON(self):
        item = model_to_dict(self)
        item['full_name'] = self.get_full_name()
        item['short_name'] = self.get_short_name()
        item['category'] = self.category.toJSON()
        item['price'] = f'{self.price:.2f}'
        item['price_promotion'] = f'{self.get_price_promotion():.2f}'
        item['price_current'] = f'{self.get_price_current():.2f}'
        item['pvp'] = f'{self.pvp:.2f}'
        item['image'] = self.get_image()
        return item

    def get_price_promotion(self):
        promotions = self.promotionsdetail_set.filter(promotion__state=True)
        if promotions.exists():
            return promotions[0].price_final
        return 0.00

    def get_price_current(self):
        price_promotion = self.get_price_promotion()
        if price_promotion > 0:
            return price_promotion
        return self.pvp

    def get_image(self):
        if self.image:
            return f'{settings.MEDIA_URL}{self.image}'
        return f'{settings.STATIC_URL}img/default/empty.png'

    def get_benefit(self):
        benefit = float(self.pvp) - float(self.price)
        return round(benefit, 2)

    def delete(self, using=None, keep_parents=False):
        try:
            os.remove(self.image.path)
        except:
            pass
        super(Product, self).delete()

    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'
        default_permissions = ()
        permissions = (
            ('view_product', 'Can view Producto'),
            ('add_product', 'Can add Producto'),
            ('change_product', 'Can change Producto'),
            ('delete_product', 'Can delete Producto'),
            ('adjust_product_stock', 'Can adjust_product_stock Producto'),
        )
        ordering = ['-name']


class Purchase(models.Model):
    number = models.CharField(max_length=8, unique=True, verbose_name='Número de factura')
    provider = models.ForeignKey(Provider, on_delete=models.PROTECT, verbose_name='Proveedor')
    payment_condition = models.CharField(choices=PAYMENT_CONDITION, max_length=50, default=PAYMENT_CONDITION[0][0], verbose_name='Condición de pago')
    date_joined = models.DateField(default=datetime.now, verbose_name='Fecha de registro')
    end_credit = models.DateField(default=datetime.now, verbose_name='Fecha de plazo de credito')
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return self.provider.name

    def calculate_invoice(self):
        subtotal = 0.00
        for i in self.purchasedetail_set.all():
            subtotal += float(i.price) * int(i.cant)
        self.subtotal = subtotal
        self.save()

    def delete(self, using=None, keep_parents=False):
        try:
            for i in self.purchasedetail_set.all():
                i.product.stock -= i.cant
                i.product.save()
                i.delete()
        except:
            pass
        super(Purchase, self).delete()

    def toJSON(self):
        item = model_to_dict(self)
        item['date_joined'] = self.date_joined.strftime('%Y-%m-%d')
        item['end_credit'] = self.end_credit.strftime('%Y-%m-%d')
        item['provider'] = self.provider.toJSON()
        item['payment_condition'] = {'id': self.payment_condition, 'name': self.get_payment_condition_display()}
        item['subtotal'] = f'{self.subtotal:.2f}'
        return item

    class Meta:
        verbose_name = 'Compra'
        verbose_name_plural = 'Compras'
        default_permissions = ()
        permissions = (
            ('view_purchase', 'Can view Compra'),
            ('add_purchase', 'Can add Compra'),
            ('delete_purchase', 'Can delete Compra'),
        )
        ordering = ['-id']


class PurchaseDetail(models.Model):
    purchase = models.ForeignKey(Purchase, on_delete=models.PROTECT)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    cant = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    dscto = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return self.product.name

    def toJSON(self):
        item = model_to_dict(self, exclude=['purchase'])
        item['product'] = self.product.toJSON()
        item['price'] = f'{self.price:.2f}'
        item['dscto'] = f'{self.dscto:.2f}'
        item['subtotal'] = f'{self.subtotal:.2f}'
        return item

    class Meta:
        verbose_name = 'Detalle de Compra'
        verbose_name_plural = 'Detalle de Compras'
        default_permissions = ()
        ordering = ['-id']


class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    mobile = models.CharField(max_length=10, unique=True, verbose_name='Teléfono')
    birthdate = models.DateField(default=datetime.now, verbose_name='Fecha de nacimiento')
    address = models.CharField(max_length=500, null=True, blank=True, verbose_name='Dirección')

    def __str__(self):
        return self.get_full_name()

    def get_full_name(self):
        return self.user.get_full_name()

    def birthdate_format(self):
        return self.birthdate.strftime('%Y-%m-%d')

    def toJSON(self):
        item = model_to_dict(self)
        item['user'] = self.user.toJSON()
        item['birthdate'] = self.birthdate.strftime('%Y-%m-%d')
        return item

    def delete(self, using=None, keep_parents=False):
        super(Client, self).delete()
        try:
            self.user.delete()
        except:
            pass

    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        ordering = ['-id']


class Sale(models.Model):
    client = models.ForeignKey(Client, on_delete=models.PROTECT, null=True, blank=True, verbose_name='Cliente')
    employee = models.ForeignKey(User, on_delete=models.PROTECT, null=True, blank=True)
    payment_condition = models.CharField(choices=PAYMENT_CONDITION, max_length=50, default=PAYMENT_CONDITION[0][0], verbose_name='Condición de pago')
    payment_method = models.CharField(choices=PAYMENT_METHOD, max_length=50, default=PAYMENT_METHOD[0][0], verbose_name='Método de pago')
    type_voucher = models.CharField(choices=VOUCHER, max_length=50, default=VOUCHER[0][0], verbose_name='Comprobante')
    date_joined = models.DateField(default=datetime.now, verbose_name='Fecha de registro')
    end_credit = models.DateField(default=datetime.now, verbose_name='Fecha limite de credito')
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name='Subtotal')
    dscto = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name='Descuento')
    total_dscto = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name='Valor del descuento')
    iva = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name='Iva')
    total_iva = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name='Valor de iva')
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name='Total a pagar')
    cash = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name='Efectivo recibido')
    change = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name='Cambio')
    card_number = models.CharField(max_length=30, null=True, blank=True, verbose_name='Número de tarjeta')
    titular = models.CharField(max_length=30, null=True, blank=True, verbose_name='Titular')
    amount_debited = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name='Monto a debitar')

    def __str__(self):
        return self.get_full_name()

    def get_full_name(self):
        return f'{self.client.user.names} / {self.get_number()}'

    def get_number(self):
        return f'{self.id:06d}'

    def card_number_format(self):
        if self.card_number:
            cardnumber = self.card_number.split(' ')
            convert = re.sub('[0-9]', 'X', ' '.join(cardnumber[1:]))
            return f'{cardnumber[0]} {convert}'
        return self.card_number

    def toJSON(self):
        item = model_to_dict(self, exclude=[''])
        item['number'] = self.get_number()
        item['card_number'] = self.card_number_format()
        item['date_joined'] = self.date_joined.strftime('%Y-%m-%d')
        item['end_credit'] = self.end_credit.strftime('%Y-%m-%d')
        item['employee'] = {} if self.employee is None else self.employee.toJSON()
        item['client'] = {} if self.client is None else self.client.toJSON()
        item['payment_condition'] = {'id': self.payment_condition, 'name': self.get_payment_condition_display()}
        item['payment_method'] = {'id': self.payment_method, 'name': self.get_payment_method_display()}
        item['type_voucher'] = {'id': self.type_voucher, 'name': self.get_type_voucher_display()}
        item['subtotal'] = f'{self.subtotal:.2f}'
        item['dscto'] = f'{self.dscto:.2f}'
        item['total_dscto'] = f'{self.total_dscto:.2f}'
        item['iva'] = f'{self.iva:.2f}'
        item['total_iva'] = f'{self.total_iva:.2f}'
        item['total'] = f'{self.total:.2f}'
        item['cash'] = f'{self.cash:.2f}'
        item['change'] = f'{self.change:.2f}'
        item['amount_debited'] = f'{self.amount_debited:.2f}'
        return item

    def calculate_invoice(self):
        subtotal = 0.00
        for i in self.saledetail_set.filter():
            i.subtotal = float(i.price) * int(i.cant)
            i.total_dscto = float(i.dscto) * float(i.subtotal)
            i.total = i.subtotal - i.total_dscto
            i.save()
            subtotal += i.total
        self.subtotal = subtotal
        self.total_iva = self.subtotal * float(self.iva)
        self.total_dscto = self.subtotal * float(self.dscto)
        self.total = float(self.subtotal) - float(self.total_dscto) + float(self.total_iva)
        self.save()

    def delete(self, using=None, keep_parents=False):
        try:
            for i in self.saledetail_set.filter(product__inventoried=True):
                i.product.stock += i.cant
                i.product.save()
                i.delete()
        except:
            pass
        super(Sale, self).delete()

    class Meta:
        verbose_name = 'Venta'
        verbose_name_plural = 'Ventas'
        default_permissions = ()
        permissions = (
            ('view_sale', 'Can view Venta'),
            ('add_sale', 'Can add Venta'),
            ('delete_sale', 'Can delete Venta'),
            ('view_sale_client', 'Can view_sale_client Venta'),
        )
        ordering = ['-id']


class SaleDetail(models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    cant = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    dscto = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total_dscto = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return self.product.name

    def toJSON(self):
        item = model_to_dict(self, exclude=['sale'])
        item['product'] = self.product.toJSON()
        item['price'] = f'{self.price:.2f}'
        item['dscto'] = f'{self.dscto:.2f}'
        item['total_dscto'] = f'{self.total_dscto:.2f}'
        item['subtotal'] = f'{self.subtotal:.2f}'
        item['total'] = f'{self.total:.2f}'
        return item

    class Meta:
        verbose_name = 'Detalle de Venta'
        verbose_name_plural = 'Detalle de Ventas'
        default_permissions = ()
        ordering = ['-id']


class CtasCollect(models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.PROTECT)
    date_joined = models.DateField(default=datetime.now)
    end_date = models.DateField(default=datetime.now)
    debt = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    saldo = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    state = models.BooleanField(default=True)

    def __str__(self):
        return self.get_full_name()

    def get_full_name(self):
        return f"{self.sale.client.user.names} ({self.sale.client.user.dni}) / {self.date_joined.strftime('%Y-%m-%d')} / ${f'{self.debt:.2f}'}"

    def validate_debt(self):
        try:
            saldo = self.paymentsctacollect_set.aggregate(result=Coalesce(Sum('valor'), 0.00, output_field=FloatField())).get('result')
            self.saldo = float(self.debt) - float(saldo)
            self.state = self.saldo > 0.00
            self.save()
        except:
            pass

    def toJSON(self):
        item = model_to_dict(self)
        item['sale'] = self.sale.toJSON()
        item['date_joined'] = self.date_joined.strftime('%Y-%m-%d')
        item['end_date'] = self.end_date.strftime('%Y-%m-%d')
        item['debt'] = f'{self.debt:.2f}'
        item['saldo'] = f'{self.saldo:.2f}'
        return item

    class Meta:
        verbose_name = 'Cuenta por cobrar'
        verbose_name_plural = 'Cuentas por cobrar'
        default_permissions = ()
        permissions = (
            ('view_ctas_collect', 'Can view Cuenta por cobrar'),
            ('add_ctas_collect', 'Can add Cuenta por cobrar'),
            ('delete_ctas_collect', 'Can delete Cuenta por cobrar'),
        )
        ordering = ['-id']


class PaymentsCtaCollect(models.Model):
    ctas_collect = models.ForeignKey(CtasCollect, on_delete=models.CASCADE, verbose_name='Cuenta por cobrar')
    date_joined = models.DateField(default=datetime.now, verbose_name='Fecha de registro')
    description = models.CharField(max_length=500, null=True, blank=True, verbose_name='Detalles')
    valor = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name='Valor')

    def __str__(self):
        return self.ctas_collect.id

    def toJSON(self):
        item = model_to_dict(self, exclude=['ctas_collect'])
        item['date_joined'] = self.date_joined.strftime('%Y-%m-%d')
        item['valor'] = f'{self.valor:.2f}'
        return item

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if self.description is None:
            self.description = 's/n'
        elif len(self.description) == 0:
            self.description = 's/n'
        super(PaymentsCtaCollect, self).save()

    class Meta:
        verbose_name = 'Pago Cuenta por cobrar'
        verbose_name_plural = 'Pagos Cuentas por cobrar'
        default_permissions = ()
        ordering = ['-id']


class DebtsPay(models.Model):
    purchase = models.ForeignKey(Purchase, on_delete=models.PROTECT)
    date_joined = models.DateField(default=datetime.now)
    end_date = models.DateField(default=datetime.now)
    debt = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    saldo = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    state = models.BooleanField(default=True)

    def __str__(self):
        return self.get_full_name()

    def get_full_name(self):
        return f"{self.purchase.provider.name} ({self.purchase.number}) / {self.date_joined.strftime('%Y-%m-%d')} / ${f'{self.debt:.2f}'}"

    def validate_debt(self):
        try:
            saldo = self.paymentsdebtspay_set.aggregate(result=Coalesce(Sum('valor'), 0.00, output_field=FloatField())).get('result')
            self.saldo = float(self.debt) - float(saldo)
            self.state = self.saldo > 0.00
            self.save()
        except:
            pass

    def toJSON(self):
        item = model_to_dict(self)
        item['purchase'] = self.purchase.toJSON()
        item['date_joined'] = self.date_joined.strftime('%Y-%m-%d')
        item['end_date'] = self.end_date.strftime('%Y-%m-%d')
        item['debt'] = f'{self.debt:.2f}'
        item['saldo'] = f'{self.saldo:.2f}'
        return item

    class Meta:
        verbose_name = 'Cuenta por pagar'
        verbose_name_plural = 'Cuentas por pagar'
        default_permissions = ()
        permissions = (
            ('view_debts_pay', 'Can view Cuenta por pagar'),
            ('add_debts_pay', 'Can add Cuenta por pagar'),
            ('delete_debts_pay', 'Can delete Cuenta por pagar'),
        )
        ordering = ['-id']


class PaymentsDebtsPay(models.Model):
    debts_pay = models.ForeignKey(DebtsPay, on_delete=models.CASCADE, verbose_name='Cuenta por pagar')
    date_joined = models.DateField(default=datetime.now, verbose_name='Fecha de registro')
    description = models.CharField(max_length=500, null=True, blank=True, verbose_name='Detalles')
    valor = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name='Valor')

    def __str__(self):
        return self.debts_pay.id

    def toJSON(self):
        item = model_to_dict(self, exclude=['debts_pay'])
        item['date_joined'] = self.date_joined.strftime('%Y-%m-%d')
        item['valor'] = f'{self.valor:.2f}'
        return item

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if self.description is None:
            self.description = 's/n'
        elif len(self.description) == 0:
            self.description = 's/n'
        super(PaymentsDebtsPay, self).save()

    class Meta:
        verbose_name = 'Det. Cuenta por pagar'
        verbose_name_plural = 'Det. Cuentas por pagar'
        default_permissions = ()
        ordering = ['-id']


class TypeExpense(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name='Nombre')

    def __str__(self):
        return self.name

    def toJSON(self):
        item = model_to_dict(self)
        return item

    class Meta:
        verbose_name = 'Tipo de Gasto'
        verbose_name_plural = 'Tipos de Gastos'
        default_permissions = ()
        permissions = (
            ('view_type_expense', 'Can view Tipo de Gasto'),
            ('add_type_expense', 'Can add Tipo de Gasto'),
            ('change_type_expense', 'Can change Tipo de Gasto'),
            ('delete_type_expense', 'Can delete Tipo de Gasto'),
        )
        ordering = ['id']


class Expenses(models.Model):
    type_expense = models.ForeignKey(TypeExpense, on_delete=models.PROTECT, verbose_name='Tipo de Gasto')
    description = models.CharField(max_length=500, null=True, blank=True, verbose_name='Descripción')
    date_joined = models.DateField(default=datetime.now, verbose_name='Fecha de Registro')
    valor = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name='Valor')

    def __str__(self):
        return self.description

    def toJSON(self):
        item = model_to_dict(self)
        item['type_expense'] = self.type_expense.toJSON()
        item['date_joined'] = self.date_joined.strftime('%Y-%m-%d')
        item['valor'] = f'{self.valor:.2f}'
        return item

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if self.description is None:
            self.description = 's/n'
        elif len(self.description) == 0:
            self.description = 's/n'
        super(Expenses, self).save()

    class Meta:
        verbose_name = 'Gasto'
        verbose_name_plural = 'Gastos'
        ordering = ['id']


class Promotions(models.Model):
    start_date = models.DateField(default=datetime.now)
    end_date = models.DateField(default=datetime.now)
    state = models.BooleanField(default=True)

    def __str__(self):
        return str(self.id)

    def toJSON(self):
        item = model_to_dict(self)
        item['start_date'] = self.start_date.strftime('%Y-%m-%d')
        item['end_date'] = self.end_date.strftime('%Y-%m-%d')
        return item

    class Meta:
        verbose_name = 'Promoción'
        verbose_name_plural = 'Promociones'
        ordering = ['-id']


class PromotionsDetail(models.Model):
    promotion = models.ForeignKey(Promotions, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    price_current = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    dscto = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total_dscto = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    price_final = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return self.product.name

    def get_dscto_real(self):
        total_dscto = float(self.price_current) * float(self.dscto)
        n = 2
        return math.floor(total_dscto * 10 ** n) / 10 ** n

    def toJSON(self):
        item = model_to_dict(self, exclude=['promotion'])
        item['product'] = self.product.toJSON()
        item['price_current'] = f'{self.price_current:.2f}'
        item['dscto'] = f'{self.dscto:.2f}'
        item['total_dscto'] = f'{self.total_dscto:.2f}'
        item['price_final'] = f'{self.price_final:.2f}'
        return item

    class Meta:
        verbose_name = 'Detalle Promoción'
        verbose_name_plural = 'Detalle de Promociones'
        default_permissions = ()
        ordering = ['-id']


class Devolution(models.Model):
    sale_detail = models.ForeignKey(SaleDetail, on_delete=models.PROTECT)
    date_joined = models.DateField(default=datetime.now, verbose_name='Fecha de registro')
    cant = models.IntegerField(default=0)
    motive = models.CharField(max_length=500, null=True, blank=True)

    def __str__(self):
        return self.motive

    def toJSON(self):
        item = model_to_dict(self)
        item['date_joined'] = self.date_joined.strftime('%Y-%m-%d')
        item['sale_detail'] = self.sale_detail.toJSON()
        item['motive'] = 'Sin detalles' if len(self.motive) == 0 else self.motive
        return item

    class Meta:
        verbose_name = 'Devolución'
        verbose_name_plural = 'Devoluciones'
        default_permissions = ()
        permissions = (
            ('view_devolution', 'Can view Devolución'),
            ('add_devolution', 'Can add Devolución'),
            ('delete_devolution', 'Can delete Devolución'),
        )
        ordering = ['-id']
