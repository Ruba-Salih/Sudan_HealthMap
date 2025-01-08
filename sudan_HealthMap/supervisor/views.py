from django.shortcuts import render, redirect
from django.contrib.auth import  logout
from django.contrib.auth.decorators import login_required
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from django.shortcuts import get_object_or_404
from hospital.models import Hospital
from hospital.serializers import HospitalSerializer
from disease.serializers import DiseaseSerializer
from disease.models import Disease
from state.models import State
from state.serializers import StateSerializer
from .utility import generate_report, generate_state_report


def supervisor_logout(request):
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
        return redirect('login_view')

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
        return redirect('login_view')

    return render(request, 'supervisor/manage_hospitals.html', {'token': token})

@login_required
def manage_reports(request):
    """
    View for managing reports.
    """
    token = request.session.get('api_token')
    if not token:
        return redirect('login_view')

    return render(request, "supervisor/manage_reports.html")

@login_required
def hospital_reports(request):
    """
    View for managing hospital reports.
    """
    token = request.session.get('api_token')
    if not token:
        return redirect('login_view')

    return render(request, "supervisor/hospital_reports.html", {'token': token})

@login_required
def simple_hospital_report(request, hospital_id):
    """
    Generate a simple report for a hospital showing disease cases.
    """
    token = request.session.get('api_token')
    if not token:
        return redirect('login_view')

    return generate_report(hospital_id, "simple", "json")

@login_required
def download_simple_report(request, hospital_id):
    """
    Generate and return the hospital report in CSV format for download.
    """
    token = request.session.get('api_token')
    if not token:
        return redirect('login_view')

    return generate_report(hospital_id, "simple", "csv")

@login_required
def detailed_hospital_report(request, hospital_id):
    """
    View a detialed report for a hospital.
    """
    token = request.session.get('api_token')
    if not token:
        return redirect('login_view')

    return generate_report(hospital_id, "detailed", "json")

@login_required
def download_detailed_report(request, hospital_id):
    """
    Generate and return the hospital report in CSV format for download.
    """
    token = request.session.get('api_token')
    if not token:
        return redirect('login_view')

    return generate_report(hospital_id, "detailed", "csv")

@login_required
def state_reports(request):
    """
    View for managing state reports.
    """
    token = request.session.get('api_token')
    if not token:
        return redirect('login_view')

    return render(request, "supervisor/state_reports.html", {'token': token})

@login_required
def state_report(request, state_id):
    """
    View for managing state reports.
    """
    token = request.session.get('api_token')
    if not token:
        return redirect('login_view')

    return generate_state_report(state_id, response_format="json")

@login_required
def download_state_report(request, state_id):
    """
    Generate and return the state report in CSV format for download.
    """
    token = request.session.get('api_token')
    if not token:
        return redirect('login_view')
    return generate_state_report(state_id, response_format="csv")


class HospitalListCreateAPIView(APIView):
    """
    API view for listing all hospitals and creating a new hospital account.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        hospitals = request.user.supervised_hospitals.all()
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
    API view for retrieving, updating, or deleting a specific hospital account.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None):
        """
        Retrieve details of a specific hospital by ID or a list of states.
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
        """
        hospital = get_object_or_404(Hospital, pk=pk, supervisor=request.user)
        hospital.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@login_required
def manage_diseases(request):
    token = request.session.get('api_token')
    if not token:
        return redirect('login_view')

    return render(request, "supervisor/manage_diseases.html", {"token": token})

class DiseaseListCreateAPIView(APIView):
    """
    API view for listing all diseases associated with the current supervisor
    and creating a new disease.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """
        Retrieve a list of all diseases created by certin supervisor.
        """
        diseases = Disease.objects.filter(created_by=request.user)
        serializer = DiseaseSerializer(diseases, many=True)
        return Response(serializer.data)

    def post(self, request):
        """
        Create a new disease.
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
        """
        disease = get_object_or_404(Disease, pk=pk, created_by=request.user)
        serializer = DiseaseSerializer(disease)
        return Response(serializer.data)

    def put(self, request, pk):
        """
        Update details of a specific disease by ID.
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

def supervisor_change_password(request):
    """
    View for supervisor user to change password
    """
    token = request.session.get('api_token')
    print(f"Token retrieved from session: {token}")
    if not token:
        return redirect('login_view')
    
    return render(request,'change_password.html', {"api_token": token, "user_type": "supervisor"})

class ChangePasswordAPIView(APIView):
    """
    API endpoint for changing the password of a supervisor.
    """
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication, SessionAuthentication]

    def post(self, request, *args, **kwargs):
        supervisor = request.user
        old_password = request.data.get("old_password")
        new_password = request.data.get("new_password")

        if not old_password or not new_password:
            return Response({"error": "Both old and new passwords are required."}, status=status.HTTP_400_BAD_REQUEST)

        if not supervisor.check_password(old_password):
            return Response({"error": "Old password is incorrect."}, status=status.HTTP_400_BAD_REQUEST)

        supervisor.set_password(new_password)
        supervisor.save()

        return Response({"message": "Password changed successfully."}, status=status.HTTP_200_OK)
