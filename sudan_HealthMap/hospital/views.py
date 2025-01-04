from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Hospital
from .hospital_tok import HospitalToken


def hospital_login(request):
    """
    View for Hospital Login
    """
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        print(f"Attempting login with email: {email}")


        try:
             hospital = Hospital.objects.get(email=email)
             print(f"Hospital found: {hospital.name}")
             if check_password(password, hospital.password):
                print("Password is valid")
                login(request, hospital, backend='hospital.auth_backend.HospitalBackend')

                token, _ = HospitalToken.objects.get_or_create(hospital=hospital)
                request.session['api_token'] = token.key

                print('ok')
                return redirect('hospital:hospital_dashboard')
             else:
                return render(request, 'login.html', {'error': 'Invalid credentials'})
        except Hospital.DoesNotExist:
            render(request, 'error.html', {'message': 'No hospital found for the logged-in user.'})
        except Exception as e:
            print(f"Unexpected error: {e}")
            return render(request, 'login.html', {'error': 'An unexpected error occurred. Please try again.'})
            
    return render(request, 'login.html')

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
        return redirect('hospital_login')
    
    return render(request,'hospital/dashboard.html', {'token': token})
