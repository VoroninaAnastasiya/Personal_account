
from django.urls import path, include

from api.views import register_new_user, register_new_product, login, get_user_profile, update_data

urlpatterns = [
    path('register/', register_new_user, name='register'),
    path('login/', login),
    path('new_product/', register_new_product),
    path('user_profile/', get_user_profile),
    path('update_data/', update_data),
]