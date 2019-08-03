from django.urls import path
from . import views


app_name = 'wechat'
urlpatterns = [
    path('', views.index, name='index'),
    path('msg_search', views.msg_search, name='msg_search'),
    path('export_excel', views.export_excel, name='export_excel'),
    path('login', views.login, name='login'),
]
