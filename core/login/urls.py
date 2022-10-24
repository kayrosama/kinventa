from django.urls import path

from core.login.views import *

urlpatterns = [
    path('', LoginAuthView.as_view(), name='login'),
    path('logout', LoginLogoutRedirectView.as_view(), name='logout'),
    path('reset/password/', LoginResetPasswordView.as_view(), name='reset_password'),
    path('update/password/<str:pk>/', LoginUpdatePasswordView.as_view(), name='update_password'),
    path('different/', LoginAuthView.as_view(), name='login_different'),
    path('authenticated/', LoginAuthenticatedView.as_view(), name='login_authenticated'),
]
