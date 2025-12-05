from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from accounts.models import DriverProfile
from accounts.forms import DriverProfileForm

@login_required
def driver_profile(request):
    profile, created = DriverProfile.objects.get_or_create(user=request.user)
    

    
    if request.method == 'POST':
        form = DriverProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('driver_profile')
    else:
        form = DriverProfileForm(instance=profile)
    
    return render(request, 'driver_profile.html', {'form': form, 'profile': profile})