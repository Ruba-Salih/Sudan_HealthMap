from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from disease.models import Disease
from .serializers import DiseaseSerializer
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from rest_framework.authentication import SessionAuthentication

def home(request):
    return HttpResponse("Welcome to the Sudan HealthMap!")

def supervisor_login(request):
    """
    Handle the login process for a supervisor.
    """
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('add_disease_form')  # Redirect to the add disease form after successful login
        else:
            return render(request, 'supervisor/login.html', {'error': 'Invalid login credentials'})

    return render(request, 'supervisor/login.html')

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def add_disease(request):
    """
    API endpoint to add a new disease. Only authenticated users can access this.
    """
    if not request.user.groups.filter(name='Supervisors').exists():
        return Response({"detail": "Permission denied. Only supervisors can add diseases."},
                        status=status.HTTP_403_FORBIDDEN)

    if request.method == 'POST':
        serializer = DiseaseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(created_by=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Handle GET request: return a list of diseases
    diseases = Disease.objects.filter(created_by=request.user)
    serializer = DiseaseSerializer(diseases, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@login_required
def add_disease_form(request):
    """
    Display a form for adding a new disease and handle form submission.
    """
    if request.method == 'POST':
        disease_name = request.POST.get('disease_name')
        cases = request.POST.get('cases')

        if disease_name and cases:
            Disease.objects.create(name=disease_name, cases=int(cases), created_by=request.user)
            return render(request, 'supervisor/add_disease.html', {'success': 'Disease added successfully!'})

        return render(request, 'supervisor/add_disease.html', {'error': 'Please fill in all fields.'})

    return render(request, 'supervisor/add_disease.html')
