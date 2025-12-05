from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.decorators import login_required
from .models import User, Profile
from listings.models import Property

def register(request):
    if request.method == 'POST':
        # Get form values
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password_confirm = request.POST['password_confirm']
        
        # Check passwords match
        if password != password_confirm:
            messages.error(request, 'Passwords do not match')
            return redirect('register')
            
        # Check username exists
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
            return redirect('register')
            
        # Check email exists
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists')
            return redirect('register')
            
        # Create user
        user = User.objects.create_user(username=username, email=email, password=password)
        user.first_name = first_name
        user.last_name = last_name
        user.save()
        
        # Create profile
        Profile.objects.create(user=user)
        
        messages.success(request, 'You are now registered and can log in')
        return redirect('login')
    else:
        return render(request, 'users/register.html')

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = auth.authenticate(username=username, password=password)
        
        if user is not None:
            auth.login(request, user)
            messages.success(request, 'You are now logged in')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid credentials')
            return redirect('login')
    else:
        return render(request, 'users/login.html')

def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        messages.success(request, 'You have been logged out')
        return redirect('index')

@login_required
def dashboard(request):
    user_inquiries = request.user.inquiry_set.all()
    
    context = {
        'inquiries': user_inquiries
    }
    
    if request.user.is_agent or request.user.is_superuser:
        if request.user.is_superuser:
            listings = Property.objects.all()
        else:
            listings = request.user.property_set.all()
        context['listings'] = listings
        
    return render(request, 'users/dashboard.html', context)
