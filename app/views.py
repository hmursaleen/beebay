from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib import messages, auth
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login, get_user_model
from django.template import loader
from .models import Blog, Comment, Profile
from django.conf import settings


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
        if len(password) < 8 or not any(c.islower() for c in password) or \
           not any(c.isupper() for c in password) or not any(c.isdigit() for c in password) or \
           not any(c in '!@#$%^&*()-_=+[{]}\|;:,<.>/?' for c in password):
            messages.error(request, 'Password must contain at least 8 characters with one lowercase letter, one uppercase letter, one digit, and one special character')
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
    blogs = Blog.objects.select_related('user').all().order_by('-posted_at')
    context = {
        'blogs': blogs,
        'MEDIA_URL': settings.MEDIA_URL
    }
    return render(request, 'dashboard.html', context)

def create_blog(request):
    if request.method == 'POST':
        content = request.POST['content']
        image = request.FILES.get('image')
        
        # Create a new blog object
        blog = Blog(user=request.user, content=content)
        
        # If an image is provided, save it to the blog object
        if image:
            blog.image = image
        
        # Save the blog object to the database
        blog.save()
        
        messages.success(request, 'Blog created successfully!')
        return redirect('dashboard')
    
    return render(request, 'dashboard.html')


@login_required
def like_blog(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id)
    if request.user in blog.likes.all():
        blog.likes.remove(request.user)
    else:
        blog.likes.add(request.user)
    likes_count = blog.likes.count()
    return JsonResponse({'likes_count': likes_count})


@login_required
def add_comment(request, blog_id):
    if request.method == 'POST':
        content = request.POST['content']
        blog = get_object_or_404(Blog, id=blog_id)
        comment = Comment(user=request.user, content=content, blog=blog)
        comment.save()
    return redirect('dashboard')


@login_required
def profile(request):
    user = request.user
    blogs = Blog.objects.filter(user=user).order_by('-posted_at')
    context = {
        'user': user,
        #'blogs': blogs,
    }
    return render(request, 'profile.html', context)



User = get_user_model()
@login_required
def edit_profile(request):
    user = request.user
    # Check if the user has a profile
    if not hasattr(user, 'Profile'):
        # Create a profile for the user
        Profile.objects.create(user=user)

    # Access the profile associated with the user
    profile = user.Profile

    if request.method == 'POST':
        description = request.POST['description']
        profile.description = description
        profile.save()
        messages.success(request, 'Profile updated successfully!')
        return redirect('profile')

    context = {
        'user': user,
    }
    return render(request, 'edit_profile.html', context)