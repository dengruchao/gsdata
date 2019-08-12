from django.urls import path
from . import views


app_name = 'wechat'
urlpatterns = [
    path('search', views.search, name='search'),
    path('result', views.result, name='result'),
    path('sort_result', views.sort_result, name='sort_result'),
    path('download', views.download, name='download'),
]
