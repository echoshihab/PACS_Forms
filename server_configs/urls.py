from django.urls import path
from . import views

urlpatterns = [
    path('', views.server_config, name='server_config'),
]
