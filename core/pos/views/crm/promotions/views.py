import json
from datetime import datetime

from django.db import transaction
from django.db.models import Q
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, FormView

from core.pos.forms import Promotions, PromotionsForm, Product, PromotionsDetail
from core.reports.forms import ReportForm
from core.security.mixins import PermissionMixin


class PromotionsListView(PermissionMixin, FormView):
    template_name = 'crm/promotions/list.html'
    form_class = ReportForm
    permission_required = 'view_promotions'

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'search':
                data = []
                start_date = request.POST['start_date']
                end_date = request.POST['start_date']
                queryset = self.get_queryset()
                if len(start_date) and len(end_date):
                    queryset = queryset.filter(start_date__range=[start_date, end_date])
                for i in queryset:
                    data.append(i.toJSON())
            elif action == 'search_detail_products':
                data = []
                for i in PromotionsDetail.objects.filter(promotion_id=request.POST['id']):
                    data.append(i.toJSON())
            else:
                data['error'] = 'No ha ingresado una opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_queryset(self):
        date_now = datetime.now().date()
        proms = Promotions.objects.filter(end_date__lte=date_now, state=True)
        if proms.exists():
            proms.update(state=False)
        return Promotions.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse_lazy('promotions_create')
        context['title'] = 'Listado de Promociones'
        return context


class PromotionsCreateView(PermissionMixin, CreateView):
    model = Promotions
    template_name = 'crm/promotions/create.html'
    form_class = PromotionsForm
    success_url = reverse_lazy('promotions_list')
    permission_required = 'add_promotions'

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'add':
                with transaction.atomic():
                    promotion = Promotions()
                    promotion.start_date = datetime.strptime(request.POST['start_date'], '%Y-%m-%d')
                    promotion.end_date = datetime.strptime(request.POST['end_date'], '%Y-%m-%d')
                    promotion.save()
                    promotion.state = promotion.end_date.date() > promotion.start_date.date()
                    promotion.save()
                    for i in json.loads(request.POST['products']):
                        product = Product.objects.get(pk=i['id'])
                        promotionsdetail = PromotionsDetail()
                        promotionsdetail.promotion_id = promotion.id
                        promotionsdetail.product_id = product.id
                        promotionsdetail.dscto = float(i['dscto']) / 100
                        promotionsdetail.price_current = float(product.pvp)
                        promotionsdetail.total_dscto = promotionsdetail.get_dscto_real()
                        promotionsdetail.price_final = float(promotionsdetail.price_current) - float(promotionsdetail.total_dscto)
                        promotionsdetail.save()
            elif action == 'search_products':
                data = []
                ids = json.loads(request.POST['ids'])
                term = request.POST['term']
                ids = ids + list(PromotionsDetail.objects.filter(promotion__state=True).values_list('product_id', flat=True))
                queryset = Product.objects.filter().exclude(id__in=ids).order_by('name')
                if len(term):
                    queryset = queryset.filter(Q(name__icontains=term) | Q(code__icontains=term))
                    queryset = queryset[0:10]
                for i in queryset:
                    item = i.toJSON()
                    item['value'] = i.get_full_name()
                    item['choose'] = False
                    data.append(item)
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['list_url'] = self.success_url
        context['title'] = 'Nuevo registro de una Promoción'
        context['action'] = 'add'
        context['products'] = []
        return context


class PromotionsUpdateView(PermissionMixin, UpdateView):
    model = Promotions
    template_name = 'crm/promotions/create.html'
    form_class = PromotionsForm
    success_url = reverse_lazy('promotions_list')
    permission_required = 'change_promotions'

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def get_form(self, form_class=None):
        instance = self.object
        date_range = f"{instance.start_date.strftime('%Y-%m-%d')} - {instance.end_date.strftime('%Y-%m-%d')}"
        form = PromotionsForm(instance=instance, initial={
            'date_range': date_range
        })
        form.fields['date_range'].initial = date_range
        return form

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'edit':
                with transaction.atomic():
                    promotion = self.object
                    promotion.start_date = datetime.strptime(request.POST['start_date'], '%Y-%m-%d')
                    promotion.end_date = datetime.strptime(request.POST['end_date'], '%Y-%m-%d')
                    promotion.save()
                    promotion.state = promotion.end_date.date() > promotion.start_date.date()
                    promotion.save()
                    promotion.promotionsdetail_set.all().delete()
                    for i in json.loads(request.POST['products']):
                        product = Product.objects.get(pk=i['id'])
                        promotionsdetail = PromotionsDetail()
                        promotionsdetail.promotion_id = promotion.id
                        promotionsdetail.product_id = product.id
                        promotionsdetail.dscto = float(i['dscto']) / 100
                        promotionsdetail.price_current = float(product.pvp)
                        promotionsdetail.total_dscto = promotionsdetail.get_dscto_real()
                        promotionsdetail.price_final = float(promotionsdetail.price_current) - float(promotionsdetail.total_dscto)
                        promotionsdetail.save()
            elif action == 'search_products':
                data = []
                ids = json.loads(request.POST['ids'])
                term = request.POST['term']
                ids = ids + list(PromotionsDetail.objects.filter(promotion__state=True).values_list('product_id', flat=True))
                queryset = Product.objects.filter().exclude(id__in=ids).order_by('name')
                if len(term):
                    queryset = queryset.filter(Q(name__icontains=term) | Q(code__icontains=term))
                    queryset = queryset[0:10]
                for i in queryset:
                    item = i.toJSON()
                    item['value'] = i.get_full_name()
                    item['choose'] = False
                    data.append(item)
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_detproducts(self):
        data = []
        try:
            for i in self.object.promotionsdetail_set.all():
                item = i.product.toJSON()
                item['dscto'] = f'{float(i.dscto) * 100:.2f}'
                item['total_dscto'] = f'{i.total_dscto:.2f}'
                item['price_current'] = f'{i.price_current:.2f}'
                item['price_final'] = f'{i.price_final:.2f}'
                data.append(item)
        except:
            pass
        return json.dumps(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['list_url'] = self.success_url
        context['title'] = 'Nueva Edición de una Promoción'
        context['action'] = 'edit'
        context['products'] = self.get_detproducts()
        return context


class PromotionsDeleteView(PermissionMixin, DeleteView):
    model = Promotions
    template_name = 'crm/promotions/delete.html'
    success_url = reverse_lazy('promotions_list')
    permission_required = 'delete_promotions'

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
