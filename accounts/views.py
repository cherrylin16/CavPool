from django.contrib.auth.decorators import login_required  # Import this first
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from allauth.socialaccount.models import SocialAccount
from .models import User
from .forms import CustomUserCreationForm


def driver_login(request):
    if request.user.is_authenticated:
        if request.user.user_type == 'driver':
            return redirect('/driver/')
        elif request.user.user_type == 'rider':
            return redirect('/rider/')
    return render(request, 'accounts/driver_login.html')


def rider_login(request):
    if request.user.is_authenticated:
        if request.user.user_type == 'driver':
            return redirect('/driver/')
        elif request.user.user_type == 'rider':
            return redirect('/rider/')
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
        pass  # Invalid role, handle accordingly
    request.session['role_intent'] = role
    return redirect('/accounts/google/login/')


@login_required
def login_redirect(request):
    user = request.user
    if user.is_staff:  # Check if moderator
        return redirect('moderator_dashboard')
    if user.user_type == 'driver':
        return redirect('/driver/')
    return redirect('/rider/')
