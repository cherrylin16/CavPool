from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse

# Create your views here.
def index(request):
    return HttpResponse("Hello, CS 3240 TA. This is Team A01 and this our Django base project deployed.")