from django.urls import path
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    # Authentication and Dashboard
    path('login/', views.supervisor_login, name='supervisor_login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.supervisor_dashboard, name='supervisor_dashboard'),

    # Manage HTML Templates
    path('manage-diseases/', views.manage_diseases, name='manage_diseases'),
    path('manage-hospitals/', views.manage_hospitals, name='manage_hospitals'),

    # API Endpoints for Diseases
    path('api/diseases/', views.DiseaseListCreateAPIView.as_view(), name='disease-list'),
    path('api/diseases/<int:pk>/', views.DiseaseRetrieveUpdateDeleteAPIView.as_view(), name='disease-detail'),

    # API Endpoints for Hospitals
    path('api/hospitals/', views.HospitalListCreateAPIView.as_view(), name='hospital-list'),
    path('api/hospitals/<int:pk>/', views.HospitalRetrieveUpdateDeleteAPIView.as_view(), name='hospital-detail'),

    # API Endpoint for States
    path('api/states/', views.StateListAPIView.as_view(), name='state-list'),
    path('error/', views.error_page, name='error_page'),
]
