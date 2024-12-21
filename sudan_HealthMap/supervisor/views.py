from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from disease.models import Disease
from .serializers import DiseaseSerializer

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
            return redirect('desired_view_after_login')  # Redirect to the desired page after successful login
        else:
            return render(request, 'supervisor/login.html', {'error': 'Invalid login credentials'})

    return render(request, 'supervisor/login.html')


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_disease(request):
    """
    API endpoint to add a new disease. Only authenticated users can access this.
    """

    if not request.user.groups.filter(name='Supervisors').exists():
        return Response({"detail": "Permission denied. Only supervisors can add diseases."}, 
                        status=status.HTTP_403_FORBIDDEN)
    
    serializer = DiseaseSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(created_by=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
