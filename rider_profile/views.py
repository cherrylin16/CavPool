from django.shortcuts import render

def rider_profile(request):
    return render(request, "rider_profile.html")