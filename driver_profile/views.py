from django.shortcuts import render

def driver_profile(request):
    return render(request, "driver_profile.html")