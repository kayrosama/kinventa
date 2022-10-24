import json

from django.db import transaction
from django.db.models import Q
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import DeleteView, CreateView, FormView

from core.pos.forms import *
from core.reports.forms import ReportForm
from core.security.mixins import PermissionMixin


class DevolutionListView(PermissionMixin, FormView):
    template_name = 'crm/devolution/list.html'
    form_class = ReportForm
    permission_required = 'view_devolution'

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'search':
                data = []
                queryset = Devolution.objects.filter()
                start_date = request.POST['start_date']
                end_date = request.POST['end_date']
                if len(start_date) and len(end_date):
                    queryset = queryset.filter(date_joined__range=[start_date, end_date])
                for i in queryset:
                    item = i.toJSON()
                    item['sale_detail']['sale'] = i.sale_detail.sale.toJSON()
                    data.append(item)
            else:
                data['error'] = 'No ha ingresado una opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Devoluciones'
        context['create_url'] = reverse_lazy('devolution_create')
        return context


class DevolutionCreateView(PermissionMixin, CreateView):
    model = Devolution
    template_name = 'crm/devolution/create.html'
    form_class = DevolutionForm
    success_url = reverse_lazy('devolution_list')
    permission_required = 'add_devolution'

    def post(self, request, *args, **kwargs):
        action = request.POST['action']
        data = {}
        try:
            if action == 'search_sale':
                data = []
                term = request.POST['term']
                for i in Sale.objects.filter(Q(client__user__names__icontains=term) | Q(client__user__dni__icontains=term))[0:10]:
                    item = i.toJSON()
                    item['text'] = i.get_full_name()
                    data.append(item)
            elif action == 'search_products_detail':
                data = []
                for i in SaleDetail.objects.filter(sale_id=request.POST['id']):
                    item = i.toJSON()
                    item['amount_return'] = 0
                    item['state'] = 0
                    item['motive'] = ''
                    data.append(item)
            elif action == 'add':
                with transaction.atomic():
                    products = json.loads(request.POST['products'])
                    for i in products:
                        devolution = Devolution()
                        devolution.sale_detail_id = int(i['id'])
                        devolution.cant = int(i['amount_return'])
                        devolution.motive = i['motive']
                        devolution.save()
                        devolution.sale_detail.cant -= devolution.cant
                        devolution.sale_detail.save()
                        devolution.sale_detail.sale.calculate_invoice()
            else:
                data['error'] = 'No ha ingresado una opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['list_url'] = self.success_url
        context['title'] = 'Nuevo registro de una Devolución'
        context['action'] = 'add'
        return context


class DevolutionDeleteView(PermissionMixin, DeleteView):
    model = Devolution
    template_name = 'crm/devolution/delete.html'
    success_url = reverse_lazy('devolution_list')
    permission_required = 'delete_devolution'

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
