from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home_page, name='home'),
    path('tech_form/', views.tech_form, name='tech_form'),
    path('tech_form_submit/', views.tech_form_submit, name='tech_form_submit'),
    path('query_worklist/', views.query_worklist, name='query_worklist'),
    path('admin_login/', auth_views.LoginView.as_view(
        template_name='tech_forms/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='tech_forms/home.html'), name='logout')

]
