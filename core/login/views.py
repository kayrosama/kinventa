import json
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.db import transaction
from django.http import HttpResponseRedirect, HttpResponse
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views.generic import FormView, RedirectView, TemplateView

from config import settings
from core.login.forms import ResetPasswordForm, UpdatePasswordForm
from core.security.models import AccessUsers
from core.user.models import User


class LoginAuthView(LoginView):
    form_class = AuthenticationForm
    template_name = 'login/login.html'

    def get_form(self, form_class=None):
        form = super(LoginAuthView, self).get_form(form_class)
        for i in form.visible_fields():
            i.field.widget.attrs.update({
                'class': 'form-control',
                'autocomplete': 'off',
                'placeholder': f'Ingrese su {i.label.lower()}'
            })
        return form

    def get(self, request, *args, **kwargs):
        login_different = reverse_lazy('login_different')
        if request.user.is_authenticated and login_different != request.path:
            return HttpResponseRedirect(reverse_lazy('login_authenticated'))
        return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        login(self.request, form.get_user())
        if self.request.user.is_authenticated:
            self.request.user.set_group_session()
            AccessUsers(user=self.request.user).save()
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Inicio de Sesión'
        return context


class LoginAuthenticatedView(TemplateView):
    template_name = 'login/login_authenticated.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class LoginResetPasswordView(FormView):
    template_name = 'login/reset_password.html'
    form_class = ResetPasswordForm
    success_url = settings.LOGIN_URL

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            form = self.get_form()
            if form.is_valid():
                self.send_email_reset_password(form.get_user())
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def send_email_reset_password(self, user):
        with transaction.atomic():
            url = settings.LOCALHOST if not settings.DEBUG else self.request.META['HTTP_HOST']
            user.is_change_password = True
            user.email_reset_token = user.generate_token()
            user.save()
            activate_account = f'http://{url}/login/update/password/{user.email_reset_token}'
            message = MIMEMultipart('alternative')
            message['Subject'] = 'Reseteo de contraseña'
            message['From'] = settings.EMAIL_HOST_USER
            message['To'] = user.email
            parameters = {
                'user': user,
                'link_reset_password': activate_account,
                'link_home': f'http://{url}'
            }
            html = render_to_string('login/password_reset_email.html', parameters)
            content = MIMEText(html, 'html')
            message.attach(content)
            server = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT)
            server.starttls()
            server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
            server.sendmail(settings.EMAIL_HOST_USER, user.email, message.as_string())
            server.quit()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Reseteo de contraseña'
        context['list_url'] = self.success_url
        return context


class LoginUpdatePasswordView(FormView):
    template_name = 'login/update_password.html'
    form_class = UpdatePasswordForm
    success_url = settings.LOGIN_URL

    def get_object(self):
        search = User.objects.filter(email_reset_token=self.kwargs['pk'], is_change_password=True)
        if search.exists():
            return search[0]
        return None

    def get(self, request, *args, **kwargs):
        if self.get_object() is not None:
            return super().get(request, *args, **kwargs)
        return HttpResponseRedirect(self.success_url)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            form = self.get_form()
            if form.is_valid():
                user = self.get_object()
                user.is_change_password = False
                user.email_reset_token = None
                user.set_password(request.POST['password'])
                user.save()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Actualización de Contraseña'
        context['list_url'] = self.success_url
        return context


class LoginLogoutRedirectView(RedirectView):
    pattern_name = 'login'

    def dispatch(self, request, *args, **kwargs):
        logout(request)
        return super().dispatch(request, *args, **kwargs)
