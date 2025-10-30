from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from accounts.models import RiderProfile, DriverProfile
from .models import CarpoolPost
from .forms import CarpoolPostForm

def rider_dashboard(request):
    profile = None
    display_name = request.user.username
    if request.user.is_authenticated:
        try:
            profile = RiderProfile.objects.get(user=request.user)
            if profile.name:
                display_name = profile.name
        except RiderProfile.DoesNotExist:
            pass
    
    posts = CarpoolPost.objects.all()
    return render(request, "dashboard/rider_dashboard.html", {
        'display_name': display_name,
        'posts': posts
    })

def driver_dashboard(request):
    profile = None
    display_name = request.user.username
    if request.user.is_authenticated:
        try:
            profile = DriverProfile.objects.get(user=request.user)
            if profile.name:
                display_name = profile.name
        except DriverProfile.DoesNotExist:
            pass
    
    posts = CarpoolPost.objects.all()
    form = CarpoolPostForm()
    return render(request, "dashboard/driver_dashboard.html", {
        'display_name': display_name, 
        'posts': posts, 
        'form': form
    })

@login_required
def create_carpool_post(request):
    if request.method == 'POST':
        form = CarpoolPostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, 'Carpool post created successfully!')
            return redirect('driver dashboard')
    return redirect('driver dashboard')

def landing(request):
    return render(request, "dashboard/landing.html")