import json

from django.db.models import Sum, FloatField
from django.db.models.functions import Coalesce
from django.http import HttpResponse
from django.views.generic import FormView

from core.pos.models import Purchase, Sale, Expenses
from core.reports.forms import ReportForm
from core.security.mixins import ModuleMixin


class ResultsReportView(ModuleMixin, FormView):
    template_name = 'results_report/report.html'
    form_class = ReportForm

    def post(self, request, *args, **kwargs):
        action = request.POST['action']
        data = {}
        try:
            if action == 'search_report':
                data = []
                start_date = request.POST['start_date']
                end_date = request.POST['end_date']

                purchase = Purchase.objects.all()
                if len(start_date) and len(end_date):
                    purchase = purchase.filter(date_joined__range=[start_date, end_date])
                purchase = float(purchase.aggregate(result=Coalesce(Sum('subtotal'), 0.00, output_field=FloatField())).get('result'))

                sale = Sale.objects.all()
                if len(start_date) and len(end_date):
                    sale = sale.filter(date_joined__range=[start_date, end_date])
                sale = float(sale.aggregate(result=Coalesce(Sum('total'), 0.00, output_field=FloatField())).get('result'))

                expenses = Expenses.objects.all()
                if len(start_date) and len(end_date):
                    expenses = expenses.filter(date_joined__range=[start_date, end_date])
                expenses = float(expenses.aggregate(result=Coalesce(Sum('valor'), 0.00, output_field=FloatField())).get('result'))

                data.append({'name': 'Compras', 'y': purchase})
                data.append({'name': 'Ventas', 'y': sale})
                data.append({'name': 'Gastos', 'y': expenses})
            else:
                data['error'] = 'No ha ingresado una opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Reporte de Resultados'
        return context
