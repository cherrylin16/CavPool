from django.shortcuts import render

def user_profile(request):
    return render(request, "profile.html", {'user': request.user})