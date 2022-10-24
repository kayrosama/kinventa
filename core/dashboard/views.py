import json
from datetime import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum, FloatField
from django.db.models.functions import Coalesce
from django.http import HttpResponse
from django.views.generic import TemplateView

from core.pos.models import Product, Sale, Client, Provider, Category, Purchase, Company
from core.reports.choices import MONTHS
from core.security.models import Dashboard


class DashboardView(LoginRequiredMixin, TemplateView):
    def get_template_names(self):
        dashboard = Dashboard.objects.filter()
        if dashboard.exists():
            if dashboard[0].layout == 1:
                return 'vtc_dashboard.html'
        return 'hzt_dashboard.html'

    def get(self, request, *args, **kwargs):
        request.user.set_group_session()
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'get_graph_stock_products':
                data = []
                for i in Product.objects.filter(stock__gt=0).order_by('-stock')[0:10]:
                    data.append([i.name, i.stock])
            elif action == 'get_graph_purchase_vs_sale':
                data = []
                year = datetime.now().year
                rows = []
                for i in MONTHS[1:]:
                    result = Sale.objects.filter(date_joined__month=i[0], date_joined__year=year).aggregate(
                        result=Coalesce(Sum('total'), 0.00, output_field=FloatField())).get('result')
                    rows.append(float(result))
                data.append({'name': 'Ventas', 'data': rows})
                rows = []
                for i in MONTHS[1:]:
                    result = Purchase.objects.filter(date_joined__month=i[0], date_joined__year=year).aggregate(
                        result=Coalesce(Sum('subtotal'), 0.00, output_field=FloatField())).get('result')
                    rows.append(float(result))
                data.append({'name': 'Compras', 'data': rows})
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Panel de administración'
        context['company'] = Company.objects.first()
        context['clients'] = Client.objects.all().count()
        context['provider'] = Provider.objects.all().count()
        context['category'] = Category.objects.filter().count()
        context['product'] = Product.objects.all().count()
        context['sale'] = Sale.objects.filter().order_by('-id')[0:10]
        return context
