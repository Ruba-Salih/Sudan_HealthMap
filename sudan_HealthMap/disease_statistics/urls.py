from django.urls import path
from . import views

urlpatterns = [
    path('', views.disease_statistics, name='disease_statistics'),
    path('api/statistics/', views.DiseaseStatisticsAPIView.as_view(), name='disease_statistics_api'),
    path('api/cases/', views.FilteredCasesAPIView.as_view(), name='filtered_cases_api'),
    
]
