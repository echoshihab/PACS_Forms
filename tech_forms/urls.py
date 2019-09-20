from django.urls import path
from . import views

urlpatterns = [
    path('', views.tech_form, name='tech_form'),
    path('tech_form_submit/', views.tech_form_submit, name='tech_form_submit')

]
