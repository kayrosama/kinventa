from config import wsgi
import json
import random
import string

from core.pos.models import *
from core.security.models import *

from datetime import date

numbers = list(string.digits)
letters = list(string.ascii_letters)
alphanumeric = numbers + letters


def insert_products():
    with open(f'{settings.BASE_DIR}/deploy/json/products.json', encoding='utf8') as json_file:
        data = json.load(json_file)
        for i in data['rows'][0:80]:
            row = i['value']
            product = Product()
            product.name = row['nombre']
            product.code = ''.join(random.choices(alphanumeric, k=8)).upper()
            product.description = 's/n'
            product.category = product.get_or_create_category(name=row['marca'])
            product.price = random.randint(1, 10)
            product.pvp = (float(product.price) * 0.12) + float(product.price)
            product.inventoried = 1
            product.save()
            print(product.name)


def insert_purchase():
    with open(f'{settings.BASE_DIR}/deploy/json/customers.json', encoding='utf8') as json_file:
        data = json.load(json_file)
        for item in data[0:20]:
            provider = Provider()
            provider.name = item['company'].upper()
            provider.ruc = f"0{''.join(random.choices(numbers, k=12))}"
            provider.mobile = f"0{''.join(random.choices(numbers, k=9))}"
            provider.address = item['country']
            provider.email = item['email']
            provider.save()
    for i in range(1, random.randint(4, 10)):
        purchase = Purchase()
        purchase.number = ''.join(random.choices(numbers, k=8))
        purchase.provider_id = random.randint(1, Provider.objects.count())
        purchase.save()

        for d in range(1, random.randint(3, 10)):
            detail = PurchaseDetail()
            detail.purchase_id = purchase.id
            detail.product_id = random.randint(1, Product.objects.all().count())
            while purchase.purchasedetail_set.filter(product_id=detail.product_id).exists():
                detail.product_id = random.randint(1, Product.objects.all().count())
            detail.cant = random.randint(1, 50)
            detail.price = detail.product.pvp
            detail.subtotal = float(detail.price) * detail.cant
            detail.save()
            detail.product.stock += detail.cant
            detail.product.save()

        purchase.calculate_invoice()
        print(i)


def insert_sale():
    with open(f'{settings.BASE_DIR}/deploy/json/customers.json', encoding='utf8') as json_file:
        data = json.load(json_file)
        for item in data[21:41]:
            user = User()
            user.names = f"{item['first']} {item['last']}"
            user.dni = f"0{''.join(random.choices(numbers, k=9))}"
            user.email = item['email']
            user.username = user.dni
            user.set_password(user.dni)
            user.save()
            user.groups.add(Group.objects.get(pk=settings.GROUPS.get('client')))
            client = Client()
            client.user = user
            client.birthdate = date(random.randint(1969, 2006), random.randint(1, 12), random.randint(1, 28))
            client.mobile = f"0{''.join(random.choices(numbers, k=9))}"
            client.address = item['country']
            client.save()
    for i in range(1, random.randint(6, 20)):
        sale = Sale()
        sale.employee_id = 1
        sale.client_id = random.randint(1, Client.objects.all().count())
        sale.iva = 0.12
        sale.save()
        for d in range(1, 8):
            numberList = list(Product.objects.filter(stock__gt=0).values_list(flat=True))
            detail = SaleDetail()
            detail.sale_id = sale.id
            detail.product_id = random.choice(numberList)
            while sale.saledetail_set.filter(product_id=detail.product_id).exists():
                detail.product_id = random.choice(numberList)
            detail.cant = random.randint(1, detail.product.stock)
            detail.price = detail.product.pvp
            detail.subtotal = float(detail.price) * detail.cant
            detail.save()
            detail.product.stock -= detail.cant
            detail.product.save()

        sale.calculate_invoice()
        sale.cash = sale.total
        sale.save()
        print(i)


insert_products()
insert_purchase()
insert_sale()
