import json

from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, FormView, View

from core.login.forms import UpdatePasswordForm
from core.security.mixins import PermissionMixin, ModuleMixin
from core.security.models import *
from core.user.forms import UserForm, ProfileForm


class UserListView(PermissionMixin, FormView):
    template_name = 'user/list.html'
    form_class = UpdatePasswordForm
    permission_required = 'view_user'

    def get_form(self, form_class=None):
        form = UpdatePasswordForm()
        form.fields['password'].label = 'Ingrese su nueva contraseña'
        return form

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'search':
                data = []
                for i in User.objects.all():
                    data.append(i.toJSON())
            elif action == 'reset_password':
                user = User.objects.get(pk=request.POST['id'])
                current_session = user == request.user
                user.create_or_update_password(password=user.dni)
                user.save()
                if current_session:
                    update_session_auth_hash(request, user)
            elif action == 'login_with_user':
                from django.contrib.auth import login
                admin = User.objects.get(pk=request.POST['id'])
                login(request, admin)
            elif action == 'update_password':
                user = User.objects.get(pk=request.POST['id'])
                current_session = user == request.user
                user.create_or_update_password(password=request.POST['password'])
                user.save()
                if current_session:
                    update_session_auth_hash(request, user)
            elif action == 'search_access':
                data = []
                for i in AccessUsers.objects.filter(user_id=request.POST['id']):
                    data.append(i.toJSON())
            else:
                data['error'] = 'No ha ingresado una opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['create_url'] = reverse_lazy('user_create')
        context['title'] = 'Listado de Usuarios'
        return context


class UserCreateView(PermissionMixin, CreateView):
    model = User
    template_name = 'user/create.html'
    form_class = UserForm
    success_url = reverse_lazy('user_list')
    permission_required = 'add_user'

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'add':
                data = self.get_form().save()
            elif action == 'validate_data':
                data = {'valid': True}
                queryset = User.objects.all()
                pattern = request.POST['pattern']
                parameter = request.POST['parameter'].strip()
                if pattern == 'dni':
                    data['valid'] = not queryset.filter(dni=parameter).exists()
                elif pattern == 'username':
                    data['valid'] = not queryset.filter(username=parameter).exists()
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
        context['title'] = 'Nuevo registro de un Usuario'
        context['action'] = 'add'
        return context


class UserUpdateView(PermissionMixin, UpdateView):
    model = User
    template_name = 'user/create.html'
    form_class = UserForm
    success_url = reverse_lazy('user_list')
    permission_required = 'change_user'

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
                queryset = User.objects.all().exclude(id=self.get_object().id)
                pattern = request.POST['pattern']
                parameter = request.POST['parameter'].strip()
                if pattern == 'dni':
                    data['valid'] = not queryset.filter(dni=parameter).exists()
                elif pattern == 'username':
                    data['valid'] = not queryset.filter(username=parameter).exists()
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
        context['title'] = 'Edición de un Usuario'
        context['action'] = 'edit'
        return context


class UserDeleteView(PermissionMixin, DeleteView):
    model = User
    template_name = 'user/delete.html'
    success_url = reverse_lazy('user_list')
    permission_required = 'delete_user'

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


class UserUpdatePasswordView(ModuleMixin, FormView):
    template_name = 'user/update_password.html'
    form_class = PasswordChangeForm
    success_url = settings.LOGIN_URL

    def get_form(self, form_class=None):
        form = PasswordChangeForm(user=self.request.user)
        for i in form.visible_fields():
            i.field.widget.attrs.update({
                'class': 'form-control',
                'autocomplete': 'off',
                'placeholder': f'Ingrese su {i.label.lower()}'
            })
        return form

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'update_password':
                form = PasswordChangeForm(user=request.user, data=request.POST)
                if form.is_valid():
                    form.save()
                    update_session_auth_hash(request, form.user)
                else:
                    data['error'] = form.errors
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Actualización de Contraseña'
        context['action'] = 'update_password'
        return context


class UserUpdateProfileView(ModuleMixin, UpdateView):
    model = User
    template_name = 'user/update_profile.html'
    form_class = ProfileForm
    success_url = settings.LOGIN_REDIRECT_URL

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        return self.request.user

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'edit':
                data = self.get_form().save()
            elif action == 'validate_data':
                data = {'valid': True}
                queryset = User.objects.all().exclude(id=request.user.id)
                pattern = request.POST['pattern']
                parameter = request.POST['parameter'].strip()
                if pattern == 'dni':
                    data['valid'] = not queryset.filter(dni=parameter).exists()
                elif pattern == 'username':
                    data['valid'] = not queryset.filter(username=parameter).exists()
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
        context['title'] = 'Actualización de datos del perfil'
        context['action'] = 'edit'
        return context


class UserChooseProfileView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        try:
            group = Group.objects.filter(id=self.kwargs['pk'])
            request.session['group'] = None if not group.exists() else group[0]
        except:
            pass
        return HttpResponseRedirect(settings.LOGIN_REDIRECT_URL)
