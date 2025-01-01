from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from rest_framework.authtoken.models import Token
from .models import Hospital


def hospital_login(request):
    """
    View for Hospital Login
    """

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, username=email, password=password)

        print(f"User: {user}, Role: {user.role if user else 'None'}")  # Log the user and role

        if user:
            if user.is_staff:
                return render(request, 'error.html', {'message': 'Supervisors cannot log in here.'})
            login(request, user)
            return redirect('hospital:hospital_dashboard')
        else:
            print("Login failed. Invalid credentials or unauthorized access.")
            messages.error(request, 'Invalid credentials or unauthorized access.')

    return render(request, 'login.html')

def logout_view(request):
    """
    Log out the hospital and clear the token.
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
    return render(request, 'base.html')

@login_required
def hospital_dashboard(request):
    """
    View for Hospital Dashboard
    """
    if request.user.role == 'hospital':
        hospital = Hospital.objects.filter(email=request.user.email).first()
        return render(request, 'hospital/dashboard.html', {'hospital': hospital})
    elif request.user.role == 'supervisor':
        return render(request, 'supervisor/dashboard.html')
    else:
        return render(request, 'error.html', {'message': 'Role not recognized.'})
