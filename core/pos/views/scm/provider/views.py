import json

from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from core.pos.forms import Provider, ProviderForm
from core.security.mixins import PermissionMixin


class ProviderListView(PermissionMixin, ListView):
    model = Provider
    template_name = 'scm/provider/list.html'
    permission_required = 'view_provider'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse_lazy('provider_create')
        context['title'] = 'Listado de Proveedores'
        return context


class ProviderCreateView(PermissionMixin, CreateView):
    model = Provider
    template_name = 'scm/provider/create.html'
    form_class = ProviderForm
    success_url = reverse_lazy('provider_list')
    permission_required = 'add_provider'

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'add':
                data = self.get_form().save()
            elif action == 'validate_data':
                data = {'valid': True}
                queryset = Provider.objects.all()
                pattern = request.POST['pattern']
                parameter = request.POST['parameter'].strip()
                if pattern == 'name':
                    data['valid'] = not queryset.filter(name__iexact=parameter).exists()
                elif pattern == 'ruc':
                    data['valid'] = not queryset.filter(ruc=parameter).exists()
                elif pattern == 'mobile':
                    data['valid'] = not queryset.filter(mobile=parameter).exists()
                elif pattern == 'email':
                    data['valid'] = not queryset.filter(email=parameter).exists()
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['list_url'] = self.success_url
        context['title'] = 'Nuevo registro de un Proveedor'
        context['action'] = 'add'
        return context


class ProviderUpdateView(PermissionMixin, UpdateView):
    model = Provider
    template_name = 'scm/provider/create.html'
    form_class = ProviderForm
    success_url = reverse_lazy('provider_list')
    permission_required = 'change_provider'

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
                queryset = Provider.objects.all().exclude(id=self.get_object().id)
                pattern = request.POST['pattern']
                parameter = request.POST['parameter'].strip()
                if pattern == 'name':
                    data['valid'] = not queryset.filter(name__iexact=parameter).exists()
                elif pattern == 'ruc':
                    data['valid'] = not queryset.filter(ruc=parameter).exists()
                elif pattern == 'mobile':
                    data['valid'] = not queryset.filter(mobile=parameter).exists()
                elif pattern == 'email':
                    data['valid'] = not queryset.filter(email=parameter).exists()
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['list_url'] = self.success_url
        context['title'] = 'Edición de un Proveedor'
        context['action'] = 'edit'
        return context


class ProviderDeleteView(PermissionMixin, DeleteView):
    model = Provider
    template_name = 'scm/provider/delete.html'
    success_url = reverse_lazy('provider_list')
    permission_required = 'delete_provider'

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
