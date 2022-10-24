from datetime import datetime

from core.pos.models import Company
from core.security.models import Dashboard


def system_information(request):
    dashboard = Dashboard.objects.first()
    parameters = {
        'dashboard': dashboard,
        'date_joined': datetime.now(),
        'menu': 'hzt_body.html' if dashboard is None else dashboard.get_template_from_layout(),
        'company': Company.objects.first()
    }
    return parameters
