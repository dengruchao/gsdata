from django.urls import path
from . import views


app_name = 'login'
urlpatterns = [
    path('', views.login_page, name='login_page'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
]