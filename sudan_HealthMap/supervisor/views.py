from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .serializers import HospitalSerializer, DiseaseSerializer
from state.serializers import StateSerializer
from hospital.models import Hospital
from disease.models import Disease
from state.models import State
from .utility import generate_report, generate_state_report



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

            token, _ = Token.objects.get_or_create(user=user)
            request.session['api_token'] = token.key

            return redirect('supervisor_dashboard')
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})

    return render(request, 'login.html')


def logout_view(request):
    """
    Log out the supervisor and clear the token.
    """
    if request.user.is_authenticated:
        Token.objects.filter(user=request.user).delete()

        logout(request)
        request.session.flush()

    return redirect('home')

def home(request):
    """
    Simple home view for the application.
    """
    return render(request, 'landing_page.html')

@login_required
def supervisor_dashboard(request):
    """
    Display the dashboard for the supervisor.
    """
    token = request.session.get('api_token')
    if not token:
        return redirect('supervisor_login')

    return render(request,'supervisor/dashboard.html', {'token': token})

def error_page(request):
    """
    Render the access denied error page.
    """
    return render(request, 'error.html', {'message': 'Access denied. Please log in with the correct role.'})

@login_required
def manage_hospitals(request):
    """
    View for managing hospitals.
    """
    token = request.session.get('api_token')
    if not token:
        return redirect('supervisor_login')

    return render(request, 'supervisor/manage_hospitals.html', {'token': token})

@login_required
def manage_reports(request):
    """
    View for managing reports.
    """
    token = request.session.get('api_token')
    if not token:
        return redirect('supervisor_login')

    return render(request, "supervisor/manage_reports.html")

@login_required
def hospital_reports(request):
    """
    View for managing hospital reports.
    """
    token = request.session.get('api_token')
    if not token:
        return redirect('supervisor_login')

    return render(request, "supervisor/hospital_reports.html", {'token': token})

@login_required
def simple_hospital_report(request, hospital_id):
    """
    Generate a simple report for a hospital showing disease cases.
    """
    token = request.session.get('api_token')
    if not token:
        return redirect('supervisor_login')
    return generate_report(hospital_id, "simple", "json")

@login_required
def download_simple_report(request, hospital_id):
    """
    Generate and return the hospital report in CSV format for download.
    """
    token = request.session.get('api_token')
    if not token:
        return redirect('supervisor_login')
    return generate_report(hospital_id, "simple", "csv")

@login_required
def detailed_hospital_report(request, hospital_id):
    """
    View a detialed report for a hospital.
    """
    token = request.session.get('api_token')
    if not token:
        return redirect('supervisor_login')
    return generate_report(hospital_id, "detailed", "json")

@login_required
def download_detailed_report(request, hospital_id):
    """
    Generate and return the hospital report in CSV format for download.
    """
    token = request.session.get('api_token')
    if not token:
        return redirect('supervisor_login')
    return generate_report(hospital_id, "detailed", "csv")

@login_required
def state_reports(request):
    """
    View for managing state reports.
    """
    token = request.session.get('api_token')
    if not token:
        return redirect('supervisor_login')

    return render(request, "supervisor/state_reports.html", {'token': token})

@login_required
def state_report(request, state_id):
    """
    View for managing state reports.
    """
    token = request.session.get('api_token')
    if not token:
        return redirect('supervisor_login')

    return generate_state_report(state_id, response_format="json")

@login_required
def download_state_report(request, state_id):
    """
    Generate and return the state report in CSV format for download.
    """
    token = request.session.get('api_token')
    if not token:
        return redirect('supervisor_login')
    return generate_state_report(state_id, response_format="csv")

class HospitalListCreateAPIView(APIView):
    """
    API view for listing all hospitals and creating a new hospital account.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        print(f"Supervisorc: {request.user}")
        hospitals = request.user.supervised_hospitals.all()
        print(f"Queryset: {hospitals.query}")
        print(f"Retrieved Hospitals: {hospitals}")
        serializer = HospitalSerializer(hospitals, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = HospitalSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            print("Validation Errors:", serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class HospitalRetrieveUpdateDeleteAPIView(APIView):
    """
    API view for retrieving, updating, or deleting a specific hospital account
    and retrieving the list of states.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None):
        """
        Retrieve details of a specific hospital by ID or a list of states.

        Args:
            pk (int): Primary key of the hospital. If None, return states list.

        Returns:
            Response: Serialized hospital details or list of states.
        """
        if pk:
            hospital = get_object_or_404(Hospital, pk=pk, supervisor=request.user)
            print(f"Supervisor from get: {request.user}, Hospitals: {hospital}")
            serializer = HospitalSerializer(hospital)
            return Response(serializer.data)
        else:
            hospitals = Hospital.objects.filter(supervisor=request.user)
            print(f"Supervisor: {request.user}, Hospitals: {hospitals}")
            serializer = HospitalSerializer(hospitals, many=True)
            return Response(serializer.data)

    def put(self, request, pk):
        """
        Update details of a specific hospital by ID.

        Args:
            pk (int): Primary key of the hospital.
            request (Request): Contains updated hospital details in JSON format.

        Returns:
            Response: Updated hospital details or validation errors.
        """
        hospital = get_object_or_404(Hospital, pk=pk, supervisor=request.user)
        serializer = HospitalSerializer(hospital, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        """
        Delete a specific hospital by ID.

        Args:
            pk (int): Primary key of the hospital.

        Returns:
            Response: HTTP 204 status on successful deletion.
        """
        hospital = get_object_or_404(Hospital, pk=pk, supervisor=request.user)
        hospital.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@login_required
def manage_diseases(request):
    # Get the token for the logged-in user
    token = request.session.get('api_token')
    if not token:
        return redirect('supervisor_login')

    return render(request, "supervisor/manage_diseases.html", {"token": token})

class DiseaseListCreateAPIView(APIView):
    """
    API view for listing all diseases associated with the logged-in supervisor
    and creating a new disease.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Retrieve a list of all diseases created by the logged-in supervisor.

        Returns:
            Response: Serialized list of diseases.
        """
        diseases = Disease.objects.filter(created_by=request.user)
        serializer = DiseaseSerializer(diseases, many=True)
        return Response(serializer.data)

    def post(self, request):
        """
        Create a new disease.

        Args:
            request (Request): Contains the disease details.
        Returns:
            Response: The created disease details or validation errors.
        """
        serializer = DiseaseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(created_by=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DiseaseRetrieveUpdateDeleteAPIView(APIView):
    """
    API view for retrieving, updating, or deleting a specific disease.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        """
        Retrieve details of a specific disease by ID.

        Args:
            pk (int): Primary key of the disease.

        Returns:
            Response: Serialized disease details.
        """
        disease = get_object_or_404(Disease, pk=pk, created_by=request.user)
        serializer = DiseaseSerializer(disease)
        return Response(serializer.data)

    def put(self, request, pk):
        """
        Update details of a specific disease by ID.

        Args:
            pk (int): Primary key of the disease.
            request (Request): Contains updated disease details.

        Returns:
            Response: Updated disease details or validation errors.
        """
        disease = get_object_or_404(Disease, pk=pk, created_by=request.user)
        serializer = DiseaseSerializer(disease, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        """
        Delete a specific disease by ID.

        Args:
            pk (int): Primary key of the disease.

        Returns:
            Response: HTTP 204 status on successful deletion.
        """
        disease = get_object_or_404(Disease, pk=pk, created_by=request.user)
        disease.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

class StateListAPIView(APIView):
    """
    API view to list all states.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Retrieve a list of all states.

        Returns:
            Response: Serialized list of states.
        """
        states = State.objects.all()
        serializer = StateSerializer(states, many=True)
        return Response(serializer.data)
