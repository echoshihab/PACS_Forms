from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_page, name='home'),
    path('tech_form/', views.tech_form, name='tech_form'),
    path('tech_form_submit/', views.tech_form_submit, name='tech_form_submit'),
    path('query_worklist/', views.query_worklist, name='query_worklist')

]
