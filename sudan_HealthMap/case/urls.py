from django.urls import path
from .views import CaseAPIView, manage_case

app_name = 'case'

urlpatterns = [
    path('api/', CaseAPIView.as_view(), name='case-list-create'),
    path('api/<int:pk>/', CaseAPIView.as_view(), name='case-detail'),
    path('manage/', manage_case, name='manage_case'),
]
