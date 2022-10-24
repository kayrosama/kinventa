import json

from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import DeleteView, FormView

from core.reports.forms import ReportForm
from core.security.mixins import PermissionMixin
from core.security.models import AccessUsers


class AccessUsersListView(PermissionMixin, FormView):
    template_name = 'access_users/list.html'
    form_class = ReportForm
    permission_required = 'view_access_users'

    def post(self, request, *args, **kwargs):
        data = {}
        action = request.POST['action']
        try:
            if action == 'search':
                data = []
                queryset = AccessUsers.objects.filter()
                start_date = request.POST['start_date']
                end_date = request.POST['end_date']
                if len(start_date) and len(end_date):
                    queryset = queryset.filter(date_joined__range=[start_date, end_date])
                for i in queryset:
                    data.append(i.toJSON())
            else:
                data['error'] = 'No ha ingresado una opción'
        except Exception as e:
            data['error'] = str(e)
        return HttpResponse(json.dumps(data), content_type='application/json')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Accesos de los usuarios'
        return context


class AccessUsersDeleteView(PermissionMixin, DeleteView):
    model = AccessUsers
    template_name = 'access_users/delete.html'
    success_url = reverse_lazy('access_users_list')
    permission_required = 'delete_access_users'

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
