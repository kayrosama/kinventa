from django.urls import path
from .views.sale_report.views import SaleReportView
from .views.purchase_report.views import PurchaseReportView
from .views.expenses_report.views import ExpensesReportView
from .views.debts_pay_report.views import DebtsPayReportView
from .views.ctas_collect_report.views import CtasCollectReportView
from .views.results_report.views import ResultsReportView
from .views.earnings_report.views import EarningsReportView

urlpatterns = [
    path('sale/', SaleReportView.as_view(), name='sale_report'),
    path('purchase/', PurchaseReportView.as_view(), name='purchase_report'),
    path('expenses/', ExpensesReportView.as_view(), name='expenses_report'),
    path('debts/pay/', DebtsPayReportView.as_view(), name='debts_pay_report'),
    path('ctas/collect/', CtasCollectReportView.as_view(), name='ctas_collect_report'),
    path('results/', ResultsReportView.as_view(), name='results_report'),
    path('earnings/', EarningsReportView.as_view(), name='earnings_report'),
]
