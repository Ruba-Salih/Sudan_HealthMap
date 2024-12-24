from django.urls import path
from .views import StateListAPIView

urlpatterns = [
    path('api/states/', StateListAPIView.as_view(), name='state-list'),
]
