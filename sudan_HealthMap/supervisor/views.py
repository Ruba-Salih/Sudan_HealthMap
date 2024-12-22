from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect, get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from disease.models import Disease
from .serializers import DiseaseSerializer
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from rest_framework.authentication import SessionAuthentication
from django.contrib import messages
from django.db.models import Q
from hospital.models import Hospital
from .forms import HospitalAccountForm
from .hospital_service import create_hospital_account


def home(request):
    return HttpResponse("Welcome to the Sudan HealthMap!")

@login_required
def supervisor_dashboard(request):
    """
    Display the dashboard for the supervisor.
    """
    return render(request, 'supervisor/dashboard.html')

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
            return redirect('supervisor_dashboard')  # Redirect to the dashboard
        else:
            return render(request, 'supervisor/login.html', {'error': 'Invalid login credentials'})

    return render(request, 'supervisor/login.html')

@login_required
def add_hospital_account(request):
    """
    View to add a hospital account.
    """
    if request.method == 'POST':
        form = HospitalAccountForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            state = form.cleaned_data['state']
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            try:
                create_hospital_account(
                    supervisor=request.user,
                    name=name,
                    state=state,
                    username=username,
                    password=password
                )
                messages.success(request, "Hospital account created successfully!")
                return redirect('supervisor_dashboard')
            except Exception as e:
                messages.error(request, f"Error creating hospital account: {e}")
    else:
        form = HospitalAccountForm()

    return render(request, 'supervisor/add_hospital_account.html', {'form': form})


@login_required
def delete_hospitals(request):
    """
    View to search and delete hospital accounts.
    """
    query = request.GET.get('query', '')
    hospitals = Hospital.objects.all()

    if query:
        hospitals = hospitals.filter(
            Q(name__icontains=query) | Q(state__name__icontains=query)
        )

    if request.method == 'POST':
        hospital_id = request.POST.get('hospital_id')  # Get hospital ID from the form
        hospital = get_object_or_404(Hospital, id=hospital_id)
        hospital.delete()
        messages.success(request, f"Hospital '{hospital.name}' has been deleted.")
        return redirect('delete_hospitals')

    return render(request, 'supervisor/delete_hospitals.html', {'hospitals': hospitals, 'query': query})


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
