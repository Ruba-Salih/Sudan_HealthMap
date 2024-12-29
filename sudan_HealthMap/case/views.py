from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import BasePermission
from rest_framework.permissions import IsAuthenticated
from .models import Case
from .serializers import CaseSerializer
from .models import Case
from .serializers import CaseSerializer
from disease.models import Disease
from hospital.models import Hospital


@login_required
def manage_case(request):
    if request.user.role != 'hospital':
        return render(request, 'error.html', {'message': 'Access denied.'})

    try:
        # Retrieve the hospital associated with the logged-in user
        hospital = Hospital.objects.get(user=request.user)
    except Hospital.DoesNotExist:
        return render(request, 'error.html', {'message': 'No associated hospital found.'})

    if request.method == 'POST':
        data = request.POST.copy()
        data['hospital'] = hospital.id  # Use the associated hospital's ID
        serializer = CaseSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            messages.success(request, "New case added successfully!")
            return redirect('hospital:hospital_dashboard')  # Redirect to the dashboard or another page
        else:
            return render(request, 'case/manage_case.html', {'errors': serializer.errors})
    else:
        diseases = Disease.objects.all()
        return render(request, 'case/manage_case.html', {'diseases': diseases})

class IsHospitalUser(BasePermission):
    """
    Custom permission to allow only hospital users to access certain views.
    """
    def has_permission(self, request, view):
        role = getattr(request.user, 'role', None)
        print(f"Permission Debug -> User: {request.user}, Role: {role}")
        return request.user.is_authenticated and role == 'hospital'
    

class CaseAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk=None):
        """
        Retrieve all cases for the authenticated hospital or a specific case if `pk` is provided.
        """
        if pk:
            try:
                case = Case.objects.get(pk=pk, hospital=request.user.hospital)
                serializer = CaseSerializer(case)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Case.DoesNotExist:
                return Response({"error": "Case not found."}, status=status.HTTP_404_NOT_FOUND)

        cases = Case.objects.filter(hospital=request.user.hospital)
        serializer = CaseSerializer(cases, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """
        Create a new case for the authenticated hospital.
        """
    def post(self, request):
        user = request.user
        print(f"Logged-in User post: {user} ({user.role})")
        try:
            hospital = user.hospitals.first()
            print(f"Associated Hospital in POST: {hospital}")
            if not hospital:
                return Response({"error": "You are not associated with a hospital."}, status=403)
        except Exception as e:
            print(f"Error fetching hospital: {e}")
            return Response({"error": "Error fetching hospital association."}, status=500)

        # Attach hospital to data
        data = request.data.copy()
        data['hospital'] = hospital.id
        print(f"POST Data with Hospital: {data}")

        # Serialize and save
        serializer = CaseSerializer(data=data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        print(f"Serializer Errors: {serializer.errors}")
        return Response(serializer.errors, status=400)

    def put(self, request, pk):
        """
        Update a specific case for the authenticated hospital.
        """
        try:
            case = Case.objects.get(pk=pk, hospital=request.user.hospital)
        except Case.DoesNotExist:
            return Response({"error": "Case not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = CaseSerializer(case, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        """
        Delete a specific case for the authenticated hospital.
        """
        try:
            case = Case.objects.get(pk=pk, hospital=request.user.hospital)
        except Case.DoesNotExist:
            return Response({"error": "Case not found."}, status=status.HTTP_404_NOT_FOUND)

        case.delete()
        return Response({"message": "Case deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
