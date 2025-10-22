from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from accounts.models import RiderProfile
from accounts.forms import RiderProfileForm

@login_required
def rider_profile(request):
    profile, created = RiderProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        form = RiderProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('rider_profile')
    else:
        form = RiderProfileForm(instance=profile)
    
    return render(request, 'rider_profile.html', {'form': form, 'profile': profile})