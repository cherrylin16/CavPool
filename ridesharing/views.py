from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    return HttpResponse("Hello, CS 3240 TA. This is Team A01 and this our Django base project deployed.")

def user_profile(request, username):
    return 