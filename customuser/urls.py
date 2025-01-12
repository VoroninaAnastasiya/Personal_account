from django.urls import path

from customuser.views import get_main_page, register, auth_login

urlpatterns = [
    path('main/', get_main_page, name='main_page'),
    path('register/', register, name='register'),
    path('login/', auth_login, name='login'),
]