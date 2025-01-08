from django.shortcuts import render, redirect
from django.contrib.auth.hashers import check_password
from django.contrib.auth import authenticate, login
from rest_framework.authtoken.models import Token
from hospital.models import Hospital
from hospital.hospital_tok import HospitalToken

def login_view(request):
    """
    Login view for supervisors and hospitals.
    """
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            token, _ = Token.objects.get_or_create(user=user)
            request.session['api_token'] = token.key
            request.session['username'] = user.get_full_name()
            return redirect('supervisor_dashboard')

        try:
            hospital = Hospital.objects.get(email=email)
            if check_password(password, hospital.password):
                login(request, hospital, backend='hospital.auth_backend.HospitalBackend')
                token, _ = HospitalToken.objects.get_or_create(hospital=hospital)
                request.session['api_token'] = token.key
                request.session['username'] = hospital.name
                return redirect('hospital:hospital_dashboard')
        except Hospital.DoesNotExist:
            pass
        except Exception as e:
            return render(request, 'login.html', {'error': 'An unexpected error occurred. Please try again.'})

        return render(request, 'login.html', {'error': 'Invalid email or password.'})

    return render(request, 'login.html')
