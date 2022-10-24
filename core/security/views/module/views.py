import json

from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, TemplateView

from core.security.forms import ModuleForm
from core.security.mixins import PermissionMixin
from core.security.models import *


class ModuleListView(PermissionMixin, TemplateView):
    template_name = 'module/list.html'
    permission_required = 'view_module'

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'search':
                data = []
                for i in Module.objects.all():
                    data.append(i.toJSON())
            else:
                data['error'] = 'No ha ingresado una opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse_lazy('module_create')
        context['title'] = 'Listado de Módulos'
        return context


class ModuleCreateView(PermissionMixin, CreateView):
    model = Module
    template_name = 'module/create.html'
    form_class = ModuleForm
    success_url = reverse_lazy('module_list')
    permission_required = 'add_module'

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'add':
                data = self.get_form().save()
            elif action == 'validate_data':
                data = {'valid': True}
                queryset = Module.objects.filter()
                pattern = request.POST['pattern']
                parameter = request.POST['parameter'].strip()
                if pattern == 'url':
                    data['valid'] = not queryset.filter(url__iexact=parameter).exists()
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['list_url'] = self.success_url
        context['title'] = 'Nuevo registro de un Módulo'
        context['action'] = 'add'
        return context


class ModuleUpdateView(PermissionMixin, UpdateView):
    model = Module
    template_name = 'module/create.html'
    form_class = ModuleForm
    success_url = reverse_lazy('module_list')
    permission_required = 'change_module'

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
                queryset = Module.objects.filter().exclude(id=self.get_object().id)
                pattern = request.POST['pattern']
                parameter = request.POST['parameter'].strip()
                if pattern == 'url':
                    data['valid'] = not queryset.filter(url__iexact=parameter).exists()
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['list_url'] = self.success_url
        context['title'] = 'Edición de una Mòdulo'
        context['action'] = 'edit'
        return context


class ModuleDeleteView(PermissionMixin, DeleteView):
    model = Module
    template_name = 'module/delete.html'
    success_url = reverse_lazy('module_list')
    permission_required = 'delete_module'

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
