from django.urls import path
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    path('login/', views.supervisor_login, name='supervisor_login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.supervisor_dashboard, name='supervisor_dashboard'),

    path('manage-diseases/', views.manage_diseases, name='manage_diseases'),
    path('manage-hospitals/', views.manage_hospitals, name='manage_hospitals'),
    path('manage-reports/', views.manage_reports, name='manage_reports'),
    path('reports/hospital/', views.hospital_reports, name='hospital_reports'),
    path('reports/state/', views.state_reports, name='state_reports'),

    path('api/diseases/', views.DiseaseListCreateAPIView.as_view(), name='disease-list'),
    path('api/diseases/<int:pk>/', views.DiseaseRetrieveUpdateDeleteAPIView.as_view(), name='disease-detail'),

    path('api/hospitals/', views.HospitalListCreateAPIView.as_view(), name='hospital-list'),
    path('api/hospitals/<int:pk>/', views.HospitalRetrieveUpdateDeleteAPIView.as_view(), name='hospital-detail'),

    path('api/states/', views.StateListAPIView.as_view(), name='state-list'),
    path('error/', views.error_page, name='error_page'),

    path('api/reports/hospital/<int:hospital_id>/simple/', views.simple_hospital_report, name='simple_hospital_report'),
    path('api/reports/hospital/<int:hospital_id>/detailed/', views.detailed_hospital_report, name='detailed_hospital_report'),
    path('reports/hospital/<int:hospital_id>/simple/download/', views.download_simple_report, name='download_simple_report'),
    path('reports/hospital/<int:hospital_id>/detailed/download/', views.download_detailed_report, name='download_detailed_report'),

    path('api/reports/state/<int:state_id>/', views.state_report, name='state_report'),
    path('reports/state/<int:state_id>/download/', views.download_state_report, name='download_state_report'),
]
