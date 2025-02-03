from django.urls import path

from customuser.views import get_main_page, register, login_user, profile_user, user_logout

urlpatterns = [
    path('main/', get_main_page, name='main_page'),
    path('register/', register, name='register'),
    path('login/', login_user, name='login'),
    path('profile/', profile_user, name='profile'),
    path('user_logout/', user_logout, name='logout'),
]