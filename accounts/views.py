from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from allauth.socialaccount.models import SocialAccount
from .models import User
from .forms import CustomUserCreationForm
from django.conf import settings


def driver_login(request):
    if request.user.is_authenticated:
        if request.user.user_type == 'driver':
            return redirect('/driver/')
        elif request.user.user_type == 'rider':
            return redirect('/rider/')
    
    if request.method == 'POST':
        from django.contrib.auth import authenticate
        username = request.POST.get('login')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            user.user_type = 'driver'
            user.save()
            login(request, user)
            return redirect('/driver/')
        else:
            messages.error(request, 'Invalid login credentials.')
    
    return render(request, 'accounts/driver_login.html')


def rider_login(request):
    if request.user.is_authenticated:
        if request.user.user_type == 'driver':
            return redirect('/driver/')
        elif request.user.user_type == 'rider':
            return redirect('/rider/')
    
    if request.method == 'POST':
        from django.contrib.auth import authenticate
        username = request.POST.get('login')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            user.user_type = 'rider'
            user.save()
            login(request, user)
            return redirect('/rider/')
        else:
            messages.error(request, 'Invalid login credentials.')
    
    return render(request, 'accounts/rider_login.html')


def driver_signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.user_type = 'driver'
            user.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('/driver/')
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/driver_signup.html', {'form': form})


def rider_signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.user_type = 'rider'
            user.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('/rider/')
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/rider_signup.html', {'form': form})


def set_user_type(request, user_type):
    if request.user.is_authenticated:
        if not request.user.user_type:
            request.user.user_type = user_type
            request.user.save()
        if 'pending_user_type' in request.session:
            del request.session['pending_user_type']
        # Redirect to appropriate dashboard
        if user_type == 'driver':
            return redirect('/driver/')
        else:
            return redirect('/rider/')
    return redirect('/')


def start_social_login(request, role):
    if role not in ['driver', 'rider']:
        return redirect('/')
    request.session['role_intent'] = role
    return redirect('/accounts/google/login/')


@login_required
def login_redirect(request):
    user = request.user

    # Check if user is a moderator
    if user.is_moderator or user.email.lower() in [
        email.lower() for email in getattr(settings, "MODERATOR_EMAILS", [])
    ]:
        if not user.is_moderator:
            user.is_moderator = True
            user.save()
        return redirect('/moderator/')

    # Check user_type for driver/rider
    if user.user_type == 'driver':
        return redirect('/driver/')
    if user.user_type == 'rider':
        return redirect('/rider/')

    # Fallback
    return redirect('/')
