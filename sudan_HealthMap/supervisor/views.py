from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect

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
            return render(request, 'login.html', {'error': 'Invalid login credentials'})

    return render(request, 'login.html')
