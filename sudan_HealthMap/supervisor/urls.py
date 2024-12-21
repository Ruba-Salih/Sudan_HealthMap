from django.urls import path
from .views import supervisor_login, add_disease

urlpatterns = [
    path('login/', supervisor_login, name='supervisor_login'),
    path('api/add-disease/', add_disease, name='add_disease'),
]
