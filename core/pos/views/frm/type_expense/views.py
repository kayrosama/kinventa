import json

from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from core.pos.forms import TypeExpense, TypeExpenseForm
from core.security.mixins import PermissionMixin


class TypeExpenseListView(PermissionMixin, ListView):
    model = TypeExpense
    template_name = 'frm/type_expense/list.html'
    permission_required = 'view_type_expense'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse_lazy('type_expense_create')
        context['title'] = 'Listado de Tipos de Gastos'
        return context


class TypeExpenseCreateView(PermissionMixin, CreateView):
    model = TypeExpense
    template_name = 'frm/type_expense/create.html'
    form_class = TypeExpenseForm
    success_url = reverse_lazy('type_expense_list')
    permission_required = 'add_type_expense'

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'add':
                data = self.get_form().save()
            elif action == 'validate_data':
                data = {'valid': True}
                queryset = TypeExpense.objects.all()
                pattern = request.POST['pattern']
                parameter = request.POST['parameter'].strip()
                if pattern == 'name':
                    data['valid'] = not queryset.filter(name__iexact=parameter).exists()
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['list_url'] = self.success_url
        context['title'] = 'Nuevo registro de un Tipo de Gasto'
        context['action'] = 'add'
        return context


class TypeExpenseUpdateView(PermissionMixin, UpdateView):
    model = TypeExpense
    template_name = 'frm/type_expense/create.html'
    form_class = TypeExpenseForm
    success_url = reverse_lazy('type_expense_list')
    permission_required = 'change_type_expense'

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'edit':
                data = self.get_form().save()
            elif action == 'validate_data':
                data = {'valid': True}
                queryset = TypeExpense.objects.all().exclude(id=self.get_object().id)
                pattern = request.POST['pattern']
                parameter = request.POST['parameter'].strip()
                if pattern == 'name':
                    data['valid'] = not queryset.filter(name__iexact=parameter).exists()
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['list_url'] = self.success_url
        context['title'] = 'Edición de un Tipo de Gasto'
        context['action'] = 'edit'
        return context


class TypeExpenseDeleteView(PermissionMixin, DeleteView):
    model = TypeExpense
    template_name = 'frm/type_expense/delete.html'
    success_url = reverse_lazy('type_expense_list')
    permission_required = 'delete_type_expense'

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
