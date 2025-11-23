from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from accounts.decorators import verified_required
from accounts.models import DriverProfile
from accounts.forms import DriverProfileForm

@verified_required
def driver_profile(request):
    profile, created = DriverProfile.objects.get_or_create(user=request.user)
    
    # If user is verified and profile doesn't have computing_id, populate it
    if request.user.is_verified and request.user.computing_id and not profile.computing_id:
        profile.computing_id = request.user.computing_id
        profile.save()
    
    if request.method == 'POST':
        form = DriverProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('driver_profile')
    else:
        form = DriverProfileForm(instance=profile)
    
    return render(request, 'driver_profile.html', {'form': form, 'profile': profile})