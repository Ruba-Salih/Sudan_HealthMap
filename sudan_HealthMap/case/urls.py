from django.urls import path
from .views import CaseAPIView, manage_case

app_name = 'case'

urlpatterns = [
    # API for list and create
    path('api/', CaseAPIView.as_view(), name='case-list-create'),
    
    # API for specific case operations (retrieve, update, delete)
    path('api/<int:pk>/', CaseAPIView.as_view(), name='case-detail'),
    
    # Template-based view for managing cases
    path('manage/', manage_case, name='manage_case'),
]
