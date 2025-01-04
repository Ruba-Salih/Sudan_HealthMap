from django.urls import path
from . import views

app_name = 'hospital'

urlpatterns = [
    path('login/', views.hospital_login, name='hospital_login'),
    path('logout/', views.hospital_logout, name='hospital_logout'),
    path('dashboard/', views.hospital_dashboard, name='hospital_dashboard'),
]
