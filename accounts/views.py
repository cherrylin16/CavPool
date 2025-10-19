from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from allauth.socialaccount.models import SocialAccount
from .models import User

def driver_login(request):
    return render(request, 'accounts/driver_login.html')

def rider_login(request):
    return render(request, 'accounts/rider_login.html')

def driver_signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.user_type = 'driver'
            user.save()
            login(request, user)
            return redirect('/dashboard/')
    else:
        form = UserCreationForm()
    return render(request, 'accounts/driver_signup.html', {'form': form})

def rider_signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.user_type = 'rider'
            user.save()
            login(request, user)
            return redirect('/dashboard/')
    else:
        form = UserCreationForm()
    return render(request, 'accounts/rider_signup.html', {'form': form})

def set_user_type(request, user_type):
    if request.user.is_authenticated:
        if not request.user.user_type:
            request.user.user_type = user_type
            request.user.save()
        if 'pending_user_type' in request.session:
            del request.session['pending_user_type']
    return redirect('/dashboard/')
