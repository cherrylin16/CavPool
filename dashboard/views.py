from django.shortcuts import render

# Create your views here.
def home_dashboard(request):
    return render(request, "dashboard/index.html")

def landing(request):
    return render(request, "dashboard/landing.html")