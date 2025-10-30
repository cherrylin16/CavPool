from django.shortcuts import render
from accounts.models import RiderProfile, DriverProfile

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
    return render(request, "dashboard/rider_dashboard.html", {'display_name': display_name})

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
    return render(request, "dashboard/driver_dashboard.html", {'display_name': display_name})

def landing(request):
    return render(request, "dashboard/landing.html")