import json

from django.http import HttpResponse
from django.views.generic import UpdateView

from config import settings
from core.security.forms import Dashboard, DashboardForm
from core.security.mixins import ModuleMixin


class DashboardUpdateView(ModuleMixin, UpdateView):
    template_name = 'dashboard/create.html'
    form_class = DashboardForm
    model = Dashboard
    success_url = settings.LOGIN_REDIRECT_URL

    def get_object(self, queryset=None):
        instance = Dashboard.objects.filter()
        if instance.exists():
            return instance[0]
        return Dashboard()

    def get_form(self, form_class=None):
        form = super(DashboardUpdateView, self).get_form(form_class)
        instance = self.get_object()
        if instance.pk is not None:
            form.instance = instance
        return form

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'edit':
                data = self.get_form().save()
            else:
                data['error'] = 'No ha ingresado una opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['list_url'] = self.success_url
        context['title'] = 'Actualización de datos del Dashboard'
        context['action'] = 'edit'
        return context
