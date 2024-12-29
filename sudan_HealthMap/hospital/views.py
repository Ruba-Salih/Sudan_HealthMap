from django.shortcuts import render, redirect
from django.contrib.auth.hashers import check_password
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Hospital
from .serializers import HospitalSerializer
from django.contrib.auth.decorators import login_required

def hospital_login(request):
    """
    View for Hospital Login
    """
    error = None
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        print("Username:", email)
        print("Password:", password)
        try:
            hospital = Hospital.objects.get(username=email)
            print("Hospital Found:", hospital)
            if check_password(password, hospital.password):
                request.session['hospital_id'] = hospital.id
                return redirect('hospital:hospital_dashboard')
            else:
                error = "Invalid username or password"
        except Hospital.DoesNotExist:
            error = "Invalid username or password"

    return render(request, 'login.html', {'error': error})

@login_required
def hospital_dashboard(request):
    """
    View for Hospital Dashboard
    """
    hospital_id = request.session.get('hospital_id')
    if 'hospital_id' not in request.session:
        return redirect('hospital_login')
    try:
        hospital = Hospital.objects.get(id=hospital_id)
        return render(request, 'hospital/dashboard.html', {'hospital': hospital})
    except Hospital.DoesNotExist:
        return redirect('hospital_login')

class HospitalListCreateAPIView(APIView):
    """
    API View for listing and creating hospitals
    """
    def get(self, request):
        hospitals = Hospital.objects.all()
        serializer = HospitalSerializer(hospitals, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = HospitalSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
