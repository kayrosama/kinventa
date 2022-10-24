import json

from django.contrib.auth.models import Group
from django.db import transaction
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, TemplateView

from config import settings
from core.pos.forms import ClientForm, User, Client
from core.security.mixins import ModuleMixin, PermissionMixin


class ClientListView(PermissionMixin, TemplateView):
    template_name = 'crm/client/list.html'
    permission_required = 'view_client'

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'search':
                data = []
                for i in Client.objects.filter():
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse_lazy('client_create')
        context['title'] = 'Listado de Clientes'
        return context


class ClientCreateView(PermissionMixin, CreateView):
    model = User
    template_name = 'crm/client/create.html'
    form_class = ClientForm
    success_url = reverse_lazy('client_list')
    permission_required = 'add_client'

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'add':
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
            elif action == 'validate_data':
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
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['list_url'] = self.success_url
        context['title'] = 'Nuevo registro de un Cliente'
        context['action'] = 'add'
        return context


class ClientUpdateView(PermissionMixin, UpdateView):
    model = Client
    template_name = 'crm/client/create.html'
    form_class = ClientForm
    success_url = reverse_lazy('client_list')
    permission_required = 'change_client'

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def get_form(self, form_class=None):
        instance = self.get_object()
        form = ClientForm(instance=instance.user, initial={
            'mobile': instance.mobile,
            'birthdate': instance.birthdate,
            'address': instance.address,
        })
        return form

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'edit':
                with transaction.atomic():
                    user = self.get_object().user
                    user.names = request.POST['names']
                    user.dni = request.POST['dni']
                    user.username = user.dni
                    if 'image-clear' in request.POST:
                        user.remove_image()
                    if 'image' in request.FILES:
                        user.image = request.FILES['image']
                    user.email = request.POST['email']
                    user.save()
                    client = self.get_object()
                    client.mobile = request.POST['mobile']
                    client.address = request.POST['address']
                    client.birthdate = request.POST['birthdate']
                    client.save()
            elif action == 'validate_data':
                data = {'valid': True}
                pattern = request.POST['pattern']
                parameter = request.POST['parameter'].strip()
                queryset = Client.objects.all().exclude(id=self.get_object().id)
                if pattern == 'dni':
                    data['valid'] = not queryset.filter(user__dni=parameter).exists()
                elif pattern == 'mobile':
                    data['valid'] = not queryset.filter(mobile=parameter).exists()
                elif pattern == 'email':
                    data['valid'] = not queryset.filter(user__email=parameter).exists()
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['list_url'] = self.success_url
        context['title'] = 'Edición de un Cliente'
        context['action'] = 'edit'
        return context


class ClientDeleteView(PermissionMixin, DeleteView):
    model = Client
    template_name = 'crm/client/delete.html'
    success_url = reverse_lazy('client_list')
    permission_required = 'delete_client'

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


class ClientUpdateProfileView(ModuleMixin, UpdateView):
    model = User
    template_name = 'crm/client/profile.html'
    form_class = ClientForm
    success_url = settings.LOGIN_REDIRECT_URL

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        return self.request.user

    def get_form(self, form_class=None):
        instance = self.get_object()
        form = ClientForm(instance=instance, initial={
            'mobile': instance.client.mobile,
            'birthdate': instance.client.birthdate,
            'address': instance.client.address,
        })
        return form

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'edit':
                with transaction.atomic():
                    user = self.get_object()
                    user.names = request.POST['names']
                    user.dni = request.POST['dni']
                    user.username = user.dni
                    if 'image-clear' in request.POST:
                        user.remove_image()
                    if 'image' in request.FILES:
                        user.image = request.FILES['image']
                    user.email = request.POST['email']
                    user.save()

                    client = user.client
                    client.user_id = user.id
                    client.mobile = request.POST['mobile']
                    client.address = request.POST['address']
                    client.birthdate = request.POST['birthdate']
                    client.save()
            elif action == 'validate_data':
                data = {'valid': True}
                pattern = request.POST['pattern']
                parameter = request.POST['parameter'].strip()
                queryset = Client.objects.all().exclude(id=self.get_object().client.id)
                if pattern == 'dni':
                    data['valid'] = not queryset.filter(user__dni=parameter).exists()
                elif pattern == 'mobile':
                    data['valid'] = not queryset.filter(mobile=parameter).exists()
                elif pattern == 'email':
                    data['valid'] = not queryset.filter(user__email=parameter).exists()
            else:
                data['error'] = 'No ha seleccionado ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['list_url'] = self.success_url
        context['title'] = 'Edición de Perfil'
        context['action'] = 'edit'
        return context
