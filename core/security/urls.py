from django.urls import path
from .views.dashboard.views import *
from .views.module_type.views import *
from .views.module.views import *
from .views.group.views import *
from .views.access_users.views import *
from .views.database_backups.views import *

urlpatterns = [
    # module_type
    path('module/type/', ModuleTypeListView.as_view(), name='module_type_list'),
    path('module/type/add/', ModuleTypeCreateView.as_view(), name='module_type_create'),
    path('module/type/update/<int:pk>/', ModuleTypeUpdateView.as_view(), name='module_type_update'),
    path('module/type/delete/<int:pk>/', ModuleTypeDeleteView.as_view(), name='module_type_delete'),
    # module
    path('module/', ModuleListView.as_view(), name='module_list'),
    path('module/add/', ModuleCreateView.as_view(), name='module_create'),
    path('module/update/<int:pk>/', ModuleUpdateView.as_view(), name='module_update'),
    path('module/delete/<int:pk>/', ModuleDeleteView.as_view(), name='module_delete'),
    # group
    path('group/', GroupListView.as_view(), name='group_list'),
    path('group/add/', GroupCreateView.as_view(), name='group_create'),
    path('group/update/<int:pk>/', GroupUpdateView.as_view(), name='group_update'),
    path('group/delete/<int:pk>/', GroupDeleteView.as_view(), name='group_delete'),
    # access
    path('access/users/', AccessUsersListView.as_view(), name='access_users_list'),
    path('access/users/delete/<int:pk>/', AccessUsersDeleteView.as_view(), name='access_users_delete'),
    # database
    path('database/backups/', DatabaseBackupsListView.as_view(), name='database_backups_list'),
    path('database/backups/add/', DatabaseBackupsCreateView.as_view(), name='database_backups_create'),
    path('database/backups/delete/<int:pk>/', DatabaseBackupsDeleteView.as_view(), name='database_backups_delete'),
    # dashboard
    path('dashboard/update/', DashboardUpdateView.as_view(), name='dashboard_update'),
]
