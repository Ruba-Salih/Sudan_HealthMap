from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.supervisor_login, name='supervisor_login'),
    path('dashboard/', views.supervisor_dashboard, name='supervisor_dashboard'),
    path('add-disease/', views.add_disease_form, name='add_disease_form'),
    path('api/add-disease/', views.add_disease, name='api_add_disease'),
    path('add-hospital-account/', views.add_hospital_account, name='add_hospital_account'),

]
