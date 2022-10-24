import json

from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, FormView

from core.pos.forms import ExpensesForm, Expenses
from core.reports.forms import ReportForm
from core.security.mixins import PermissionMixin


class ExpensesListView(PermissionMixin, FormView):
    template_name = 'frm/expenses/list.html'
    form_class = ReportForm
    permission_required = 'view_expenses'

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'search':
                data = []
                queryset =  Expenses.objects.filter()
                start_date = request.POST['start_date']
                end_date = request.POST['end_date']
                if len(start_date) and len(end_date):
                    queryset =  queryset.filter(date_joined__range=[start_date, end_date])
                for i in queryset:
                    data.append(i.toJSON())
            else:
                data['error'] = 'No ha ingresado una opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse_lazy('expenses_create')
        context['title'] = 'Listado de Gastos'
        return context


class ExpensesCreateView(PermissionMixin, CreateView):
    model = Expenses
    template_name = 'frm/expenses/create.html'
    form_class = ExpensesForm
    success_url = reverse_lazy('expenses_list')
    permission_required = 'add_expenses'

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'add':
                data = self.get_form().save()
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['list_url'] = self.success_url
        context['title'] = 'Nuevo registro de un Gasto'
        context['action'] = 'add'
        return context


class ExpensesUpdateView(PermissionMixin, UpdateView):
    model = Expenses
    template_name = 'frm/expenses/create.html'
    form_class = ExpensesForm
    success_url = reverse_lazy('expenses_list')
    permission_required = 'change_expenses'

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'edit':
                data = self.get_form().save()
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['list_url'] = self.success_url
        context['title'] = 'Edición de un Gasto'
        context['action'] = 'edit'
        return context


class ExpensesDeleteView(PermissionMixin, DeleteView):
    model = Expenses
    template_name = 'frm/expenses/delete.html'
    success_url = reverse_lazy('expenses_list')
    permission_required = 'delete_expenses'

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
