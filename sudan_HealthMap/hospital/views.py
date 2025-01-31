from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth.decorators import login_required
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework import status
from case.models import Case
from .hospital_tok import HospitalTokenAuthentication


@login_required
def hospital_logout(request):
    """
    Log out the hospital and clear the token.
    """
    if request.user.is_authenticated:
        request.user.hospitaltoken.delete()

        logout(request)
        request.session.flush()
    return redirect('home')

def home(request):
    """
    Simple home view for the application.
    """
    return render(request, 'landing_page.html')

@login_required
def hospital_dashboard(request):
    """
    View for Hospital Dashboard
    """
    print('ok2')
    token = request.session.get('api_token')
    if not token:
        return redirect('login_view')
    
    return render(request,'hospital/dashboard.html', {'token': token})

def hospital_report(request):
    """
    View for Hospital Reports
    """
    token = request.session.get('api_token')
    print(f"Token retrieved from session: {token}")
    if not token:
        return redirect('login_view')
    
    return render(request,'hospital/manage_reports.html', {'api_token': token})

class HospitalReportAPIView(APIView):
    """
    API endpoint to fetch case reports for a specific disease in the hospital.
    """

    permission_classes = [IsAuthenticated]
    authentication_classes = [HospitalTokenAuthentication]
    renderer_classes = [JSONRenderer]

    def get(self, request, *args, **kwargs):
        hospital = request.user
        disease_id = request.query_params.get("disease_id")
        
        if not disease_id:
            return Response({"error": "Disease ID is required."}, status=400)

        cases = Case.objects.filter(
            hospital=hospital, disease_id=disease_id
        ).values(
            "patient_number",
            "patient_age",
            "patient_sex",
            "patient_blood_type",
            "patient_status",
            "main_symptom_causing_death",
            "season",
            "date_reported",
        )

        return Response(list(cases), status=200)


def hospital_change_password(request):
    """
    View for Hospital user to change password
    """
    token = request.session.get('api_token')
    print(f"Token retrieved from session: {token}")
    if not token:
        return redirect('login_view')
    
    return render(request,'change_password.html', {"api_token": token, "user_type": "hospital"})

class ChangePasswordAPIView(APIView):
    """
    API endpoint for changing the password of a hospital.
    """
    permission_classes = [IsAuthenticated]
    authentication_classes = [HospitalTokenAuthentication]

    def post(self, request, *args, **kwargs):
        hospital = request.user
        old_password = request.data.get("old_password")
        new_password = request.data.get("new_password")

        if not old_password or not new_password:
            return Response({"error": "Both old and new passwords are required."}, status=status.HTTP_400_BAD_REQUEST)

        if not check_password(old_password, hospital.password):
            return Response({"error": "Old password is incorrect."}, status=status.HTTP_400_BAD_REQUEST)

        hospital.password = make_password(new_password)
        hospital.save()

        return Response({"message": "Password changed successfully."}, status=status.HTTP_200_OK)
