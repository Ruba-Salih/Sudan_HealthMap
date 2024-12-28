from django.urls import path
from . import views

app_name = 'hospital'

urlpatterns = [
    path('login/', views.hospital_login, name='hospital_login'),
    path('dashboard/', views.hospital_dashboard, name='hospital_dashboard'),
    path('api/hospitals/', views.HospitalListCreateAPIView.as_view(), name='hospital_api'),
]
