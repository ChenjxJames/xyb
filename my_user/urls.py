from django.urls import path
from my_user import views

urlpatterns = [
    path('', views.index),
    path('login', views.login),
    path('islogin', views.login_status),
    path('logout', views.logout),
    path('register', views.register),
    path('reset_password', views.reset_password),
    path('reset_password_by_phone', views.reset_password_by_phone),
    path('identify_code', views.identify_code),
    path('user_info', views.user_info),
    path('user_protocol', views.user_protocol),
    path('add_price', views.add_price),
    path('set_info', views.set_info),
]
