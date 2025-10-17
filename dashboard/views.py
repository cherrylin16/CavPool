from django.shortcuts import render

# Create your views here.
def rider_dashboard(request):
    return render(request, "dashboard/rider_dashboard.html")

def driver_dashboard(request):
    return render(request, "dashboard/driver_dashboard.html")

def landing(request):
    return render(request, "dashboard/landing.html")