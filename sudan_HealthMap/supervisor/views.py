from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .serializers import HospitalSerializer, DiseaseSerializer
from state.serializers import StateSerializer
from hospital.models import Hospital
from disease.models import Disease
from state.models import State


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
            messages.error(request, "Invalid login credentials.")
            return render(request, 'supervisor/login.html')

    return render(request, 'supervisor/login.html')

def home(request):
    """
    Simple home view for the application.
    """
    return HttpResponse("Welcome to the Sudan HealthMap!")

@login_required
def supervisor_dashboard(request):
    """
    Display the dashboard for the supervisor.
    """
    return render(request, 'supervisor/dashboard.html')


class HospitalListCreateAPIView(APIView):
    """
    API view for listing all hospitals and creating a new hospital account.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        hospitals = Hospital.objects.filter(supervisor=request.user)
        serializer = HospitalSerializer(hospitals, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = HospitalSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(supervisor=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
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
        hospital = get_object_or_404(Hospital, pk=pk, supervisor=request.user)
        serializer = HospitalSerializer(hospital)
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
