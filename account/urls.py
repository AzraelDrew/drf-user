from django.urls import path
from . import api

urlpatterns = [
    path('users', api.UserCreateView.as_view(), name='account-create'),
    path('login',api.LoginView.as_view(),name='user-login')
]