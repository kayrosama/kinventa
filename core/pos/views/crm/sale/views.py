import json

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Group
from django.db import transaction
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.template.loader import get_template
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView, DeleteView, FormView
from weasyprint import HTML, CSS

from core.pos.forms import *
from core.reports.forms import ReportForm
from core.security.mixins import PermissionMixin


class SaleListView(PermissionMixin, FormView):
    template_name = 'crm/sale/admin/list.html'
    form_class = ReportForm
    permission_required = 'view_sale'

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'search':
                data = []
                start_date = request.POST['start_date']
                end_date = request.POST['end_date']
                queryset = Sale.objects.filter()
                if len(start_date) and len(end_date):
                    queryset = queryset.filter(date_joined__range=[start_date, end_date])
                for i in queryset:
                    data.append(i.toJSON())
            elif action == 'search_detail_products':
                data = []
                for i in SaleDetail.objects.filter(sale_id=request.POST['id']):
                    data.append(i.toJSON())
            else:
                data['error'] = 'No ha ingresado una opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse_lazy('sale_admin_create')
        context['title'] = 'Listado de Ventas'
        return context


class SaleCreateView(PermissionMixin, CreateView):
    model = Sale
    template_name = 'crm/sale/admin/create.html'
    form_class = SaleForm
    success_url = reverse_lazy('sale_admin_list')
    permission_required = 'add_sale'

    def get_form(self, form_class=None):
        form = SaleForm()
        client = Client.objects.filter(user__dni='9999999999')
        if client.exists():
            client = client[0]
            form.fields['client'].queryset = Client.objects.filter(id=client.id)
            form.initial = {'client': client}
        return form

    def post(self, request, *args, **kwargs):
        action = request.POST['action']
        data = {}
        try:
            if action == 'add':
                with transaction.atomic():
                    sale = Sale()
                    sale.employee_id = request.user.id
                    sale.client_id = int(request.POST['client'])
                    sale.payment_method = request.POST['payment_method']
                    sale.payment_condition = request.POST['payment_condition']
                    sale.type_voucher = request.POST['type_voucher']
                    sale.iva = float(Company.objects.first().iva) / 100
                    sale.dscto = float(request.POST['dscto']) / 100
                    sale.save()
                    for i in json.loads(request.POST['products']):
                        product = Product.objects.get(pk=i['id'])
                        saledetail = SaleDetail()
                        saledetail.sale_id = sale.id
                        saledetail.product_id = product.id
                        saledetail.price = float(i['price_current'])
                        saledetail.cant = int(i['cant'])
                        saledetail.subtotal = saledetail.price * saledetail.cant
                        saledetail.dscto = float(i['dscto']) / 100
                        saledetail.total_dscto = saledetail.dscto * saledetail.subtotal
                        saledetail.total = saledetail.subtotal - saledetail.total_dscto
                        saledetail.save()

                        saledetail.product.stock -= saledetail.cant
                        saledetail.product.save()
                    sale.calculate_invoice()
                    if sale.payment_condition == PAYMENT_CONDITION[1][0]:
                        sale.end_credit = request.POST['end_credit']
                        sale.cash = 0.00
                        sale.change = 0.00
                        sale.save()
                        ctascollect = CtasCollect()
                        ctascollect.sale_id = sale.id
                        ctascollect.date_joined = sale.date_joined
                        ctascollect.end_date = sale.end_credit
                        ctascollect.debt = sale.total
                        ctascollect.saldo = sale.total
                        ctascollect.save()
                    elif sale.payment_condition == PAYMENT_CONDITION[0][0]:
                        if sale.payment_method == PAYMENT_METHOD[0][0]:
                            sale.cash = float(request.POST['cash'])
                            sale.change = float(sale.cash) - sale.total
                            sale.save()
                        elif sale.payment_method == PAYMENT_METHOD[1][0]:
                            sale.card_number = request.POST['card_number']
                            sale.titular = request.POST['titular']
                            sale.amount_debited = float(request.POST['amount_debited'])
                            sale.save()
                        elif sale.payment_method == PAYMENT_METHOD[2][0]:
                            sale.cash = float(request.POST['cash'])
                            sale.card_number = request.POST['card_number']
                            sale.titular = request.POST['titular']
                            sale.amount_debited = float(request.POST['amount_debited'])
                            sale.save()
                    print_url = reverse_lazy('sale_admin_print_invoice', kwargs={'pk': sale.id})
                    data = {'print_url': str(print_url)}
            elif action == 'search_products':
                ids = json.loads(request.POST['ids'])
                data = []
                term = request.POST['term']
                queryset = Product.objects.filter(Q(stock__gt=0) | Q(inventoried=False)).exclude(id__in=ids).order_by('name')
                if len(term):
                    queryset = queryset.filter(Q(name__icontains=term) | Q(code__icontains=term))
                    queryset = queryset[:10]
                for i in queryset:
                    item = i.toJSON()
                    item['value'] = i.get_full_name()
                    item['dscto'] = '0.00'
                    item['total_dscto'] = '0.00'
                    data.append(item)
            elif action == 'search_client':
                data = []
                term = request.POST['term']
                for i in Client.objects.filter(Q(user__names__icontains=term) | Q(user__dni__icontains=term)).order_by('user__names')[0:10]:
                    item = i.toJSON()
                    item['text'] = i.get_full_name()
                    data.append(item)
            elif action == 'validate_client':
                data = {'valid': True}
                pattern = request.POST['pattern']
                parameter = request.POST['parameter'].strip()
                queryset = Client.objects.all()
                if pattern == 'dni':
                    data['valid'] = not queryset.filter(user__dni=parameter).exists()
                elif pattern == 'mobile':
                    data['valid'] = not queryset.filter(mobile=parameter).exists()
                elif pattern == 'email':
                    data['valid'] = not queryset.filter(user__email=parameter).exists()
            elif action == 'create_client':
                with transaction.atomic():
                    user = User()
                    user.names = request.POST['names']
                    user.dni = request.POST['dni']
                    user.username = user.dni
                    if 'image' in request.FILES:
                        user.image = request.FILES['image']
                    user.create_or_update_password(user.dni)
                    user.email = request.POST['email']
                    user.save()

                    client = Client()
                    client.user_id = user.id
                    client.mobile = request.POST['mobile']
                    client.address = request.POST['address']
                    client.birthdate = request.POST['birthdate']
                    client.save()

                    group = Group.objects.get(pk=settings.GROUPS.get('client'))
                    user.groups.add(group)

                    data = Client.objects.get(pk=client.id).toJSON()
            elif action == 'create_proforma':
                items = json.loads(request.POST['items'])
                template = get_template('crm/sale/print/proforma.html')
                html_template = template.render({'sale': items, 'company': Company.objects.first()}).encode(encoding="UTF-8")
                url_css = os.path.join(settings.BASE_DIR, 'static/lib/bootstrap-4.6.0/css/bootstrap.min.css')
                pdf_file = HTML(string=html_template, base_url=request.build_absolute_uri()).write_pdf(
                    stylesheets=[CSS(url_css)], presentational_hints=True)
                response = HttpResponse(pdf_file, content_type='application/pdf')
                return response
            else:
                data['error'] = 'No ha ingresado una opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['frmClient'] = ClientForm()
        context['list_url'] = self.success_url
        context['title'] = 'Nuevo registro de una Venta'
        context['action'] = 'add'
        return context


class SaleDeleteView(PermissionMixin, DeleteView):
    model = Sale
    template_name = 'crm/sale/admin/delete.html'
    success_url = reverse_lazy('sale_admin_list')
    permission_required = 'delete_sale'

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            self.get_object().delete()
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Notificación de eliminación'
        context['list_url'] = self.success_url
        return context


class SalePrintInvoiceView(LoginRequiredMixin, View):
    success_url = reverse_lazy('sale_admin_list')

    def get_success_url(self):
        if self.request.user.is_client():
            return reverse_lazy('sale_client_list')
        return self.success_url

    def get_height_ticket(self):
        sale = Sale.objects.get(pk=self.kwargs['pk'])
        height = 450
        increment = sale.saledetail_set.all().count() * 10
        height += increment
        return round(height)

    def get(self, request, *args, **kwargs):
        try:
            sale = Sale.objects.get(pk=self.kwargs['pk'])
            context = {'sale': sale, 'company': Company.objects.first()}
            if sale.type_voucher == VOUCHER[0][0]:
                template = get_template('crm/sale/print/ticket.html')
                context['height'] = self.get_height_ticket()
            else:
                template = get_template('crm/sale/print/invoice.html')
            html_template = template.render(context).encode(encoding="UTF-8")
            url_css = os.path.join(settings.BASE_DIR, 'static/lib/bootstrap-4.6.0/css/bootstrap.min.css')
            pdf_file = HTML(string=html_template, base_url=request.build_absolute_uri()).write_pdf(stylesheets=[CSS(url_css)], presentational_hints=True)
            return HttpResponse(pdf_file, content_type='application/pdf')
        except:
            pass
        return HttpResponseRedirect(self.get_success_url())


class SaleClientListView(PermissionMixin, FormView):
    template_name = 'crm/sale/client/list.html'
    form_class = ReportForm
    permission_required = 'view_sale_client'

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'search':
                data = []
                start_date = request.POST['start_date']
                end_date = request.POST['end_date']
                queryset = Sale.objects.filter(client__user_id=request.user.id)
                if len(start_date) and len(end_date):
                    queryset = queryset.filter(date_joined__range=[start_date, end_date])
                for i in queryset:
                    data.append(i.toJSON())
            elif action == 'search_detail_products':
                data = []
                for i in SaleDetail.objects.filter(sale_id=request.POST['id']):
                    data.append(i.toJSON())
            else:
                data['error'] = 'No ha ingresado una opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Ventas'
        return context
