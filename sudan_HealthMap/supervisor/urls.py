from django.urls import path
from django.views.generic import TemplateView
from . import views

urlpatterns = [
    path('login/', views.supervisor_login, name='supervisor_login'),
    path('dashboard/', views.supervisor_dashboard, name='supervisor_dashboard'),
     path('manage-diseases/', TemplateView.as_view(template_name="supervisor/manage_diseases.html"), name='manage_diseases'),

    path('api/diseases/', views.DiseaseListCreateAPIView.as_view(), name='disease-list'),
    path('api/diseases/<int:pk>/', views.DiseaseRetrieveUpdateDeleteAPIView.as_view(), name='disease-detail'),
    path('api/hospitals/', views.HospitalListCreateAPIView.as_view(), name='hospital-list'),
    path('api/hospitals/<int:pk>/', views.HospitalRetrieveUpdateDeleteAPIView.as_view(), name='hospital-detail'),
    
]
