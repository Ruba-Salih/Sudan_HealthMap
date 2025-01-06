from django.urls import path
from . import views

app_name = 'hospital'

urlpatterns = [
    path('login/', views.hospital_login, name='hospital_login'),
    path('logout/', views.hospital_logout, name='hospital_logout'),
    path('dashboard/', views.hospital_dashboard, name='hospital_dashboard'),
    
    path('hospital/reports/', views.hospital_report, name='hospital_report'),
    path('api/hospital/reports/', views.HospitalReportAPIView.as_view(), name='hospital_reports'),

    path('change-password/', views.hospital_change_password, name='change_password'),
    path('api/change-password/', views.ChangePasswordAPIView.as_view(), name='change_password'),
]
