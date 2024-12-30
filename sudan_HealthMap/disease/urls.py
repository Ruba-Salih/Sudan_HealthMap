from django.urls import path
from .views import DiseaseListAPIView

app_name = 'disease'

urlpatterns = [
    path('api/', DiseaseListAPIView.as_view(), name='disease-list'),
]
