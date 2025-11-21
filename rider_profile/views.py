from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from accounts.decorators import verified_required
from accounts.models import RiderProfile
from accounts.forms import RiderProfileForm

@verified_required
def rider_profile(request):
    profile, created = RiderProfile.objects.get_or_create(user=request.user)
    
    # If user is verified and profile doesn't have computing_id, populate it
    if request.user.is_verified and request.user.computing_id and not profile.computing_id:
        profile.computing_id = request.user.computing_id
        profile.save()
    
    if request.method == 'POST':
        form = RiderProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('rider_profile')
    else:
        form = RiderProfileForm(instance=profile)
    
    return render(request, 'rider_profile.html', {'form': form, 'profile': profile})