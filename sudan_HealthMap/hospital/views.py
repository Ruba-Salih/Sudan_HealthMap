from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Hospital


def hospital_login(request):
    """
    View for Hospital Login
    """

    if request.method == 'POST':
        username = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        print(f"User: {user}, Role: {user.role if user else 'None'}")  # Log the user and role

        if user is not None and user.role == 'hospital':
            login(request, user)
            print("Hospital login successful.")
            return redirect('hospital:hospital_dashboard')
        else:
            print("Login failed. Invalid credentials or unauthorized access.")
            messages.error(request, 'Invalid credentials or unauthorized access.')

    return render(request, 'login.html')

def logout_view(request):
    logout(request)
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

    try:
        # Check if the logged-in user has an associated hospital
        print(f"Logged-in User: {request.user}, Role: {request.user.role}")
        hospital = get_object_or_404(Hospital, user=request.user)
        return render(request, 'hospital/dashboard.html', {'hospital': hospital})
    except Hospital.DoesNotExist:
        # Log the issue if no associated hospital is found
        print(f"No hospital found for user: {request.user}")
        return render(request, 'error.html', {'message': 'No hospital found for this user.'})
