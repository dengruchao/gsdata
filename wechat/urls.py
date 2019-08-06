from django.urls import path
from . import views


app_name = 'wechat'
urlpatterns = [
    path('search', views.search, name='search'),
    path('export_excel', views.export_excel, name='export_excel'),
]
