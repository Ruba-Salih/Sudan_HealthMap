from django.urls import path
from .views import supervisor_login, add_disease
from . import views

urlpatterns = [
    path('login/', supervisor_login, name='supervisor_login'),
    path('add-disease/', views.add_disease_form, name='add_disease_form'),
    path('api/add-disease/', add_disease, name='api_add_disease'),
]
