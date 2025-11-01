from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

@login_required
def message_page(request):
    return render(request, 'message_page.html')