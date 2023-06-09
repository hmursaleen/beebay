from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login

def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        password = request.POST['password']

        # Check if username already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username is already taken')
            return redirect('signup')

        # Validate password format
        if not any(c.islower() for c in password) or \
           not any(c.isupper() for c in password) or not any(c.isdigit() for c in password) or \
           not any(c in '!@#$%^&*()-_=+[{]}\|;:,<.>/?' for c in password):
            messages.error(request, 'Password must contain at least one lowercase letter, one uppercase letter, one digit, and one special character')
            return redirect('signup')

        # Create a new user
        user = User.objects.create_user(username=username, first_name=firstname, last_name=lastname, password=password)
        user.save()

        messages.success(request, 'Signup successful! You can now log in.')
        return redirect('login')

    return render(request, 'signup.html')


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        # Authenticate user
        user = authenticate(username=username, password=password)

        if user is not None:
            # Log in the user
            auth_login(request, user)
            messages.success(request, 'Login successful!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password')
            return redirect('login')

    return render(request, 'login.html')


@login_required
def dashboard(request):
    return render(request, 'dashboard.html')