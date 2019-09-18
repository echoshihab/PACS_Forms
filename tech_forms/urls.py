from django.urls import path
from . import views

urlpatterns = [
    path('', views.tech_form, name='tech_form'),

]
