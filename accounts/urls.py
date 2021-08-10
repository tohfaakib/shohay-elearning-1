from django.urls import path, include
from .views import CreateAccount, AllUsers, CurrentUser, CustomLogin, ChangePasswordView, ResetPasswordRequest, ResetPasswordConfirm

app_name = 'users'

urlpatterns = [
    path('auth/registration/', CreateAccount.as_view(), name="registration"),
    path('auth/login/', CustomLogin.as_view(), name="custom-login"),
    path('users/all/', AllUsers.as_view(), name="all"),
    path('user/current-user/', CurrentUser.as_view(), name="current"),
    path('auth/change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('auth/reset-password/', ResetPasswordRequest.as_view(), name='reset-pass-request'),
    path('auth/reset-password/confirm/', ResetPasswordConfirm.as_view(), name='reset-pass-confirm'),
]
