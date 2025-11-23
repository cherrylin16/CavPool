from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from allauth.socialaccount.models import SocialAccount
from .models import User, DriverProfile, RiderProfile
from .forms import CustomUserCreationForm
from django.conf import settings
from django.core.mail import send_mail
from django.urls import reverse
import secrets


def driver_login(request):
    if request.user.is_authenticated:
        if not request.user.is_verified:
            request.session['login_type'] = 'driver'
            return redirect('verification')
        if request.user.user_type == 'driver':
            return redirect('/driver/')
        elif request.user.user_type == 'rider':
            return redirect('/rider/')
    
    if request.method == 'POST':
        username = request.POST.get('login')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # Check if user has a driver profile
            if not DriverProfile.objects.filter(user=user).exists():
                messages.error(request, 'No driver profile found for this account.')
                return render(request, 'accounts/driver_login.html')
            
            # Check if user is verified
            if not user.is_verified:
                user.user_type = 'driver'
                user.save()
                login(request, user)
                request.session['login_type'] = 'driver'
                return redirect('verification')
            
            user.user_type = 'driver'
            user.save()
            login(request, user)
            return redirect('/driver/')
        else:
            messages.error(request, 'Invalid login credentials.')
    
    return render(request, 'accounts/driver_login.html')


def rider_login(request):
    if request.user.is_authenticated:
        if not request.user.is_verified:
            request.session['login_type'] = 'rider'
            return redirect('verification')
        if request.user.user_type == 'driver':
            return redirect('/driver/')
        elif request.user.user_type == 'rider':
            return redirect('/rider/')
    
    if request.method == 'POST':
        username = request.POST.get('login')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # Check if user has a rider profile
            if not RiderProfile.objects.filter(user=user).exists():
                messages.error(request, 'No rider profile found for this account.')
                return render(request, 'accounts/rider_login.html')
            
            # Check if user is verified
            if not user.is_verified:
                user.user_type = 'rider'
                user.save()
                login(request, user)
                request.session['login_type'] = 'rider'
                return redirect('verification')
            
            user.user_type = 'rider'
            user.save()
            login(request, user)
            return redirect('/rider/')
        else:
            messages.error(request, 'Invalid login credentials.')
    
    return render(request, 'accounts/rider_login.html')


def driver_signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.user_type = 'driver'
            user.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            request.session['login_type'] = 'driver'
            return redirect('verification')
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/driver_signup.html', {'form': form})


def rider_signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.user_type = 'rider'
            user.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            request.session['login_type'] = 'rider'
            return redirect('verification')
    else:
        form = CustomUserCreationForm()
    return render(request, 'accounts/rider_signup.html', {'form': form})


def set_user_type(request, user_type):
    if request.user.is_authenticated:
        if not request.user.user_type:
            request.user.user_type = user_type
            request.user.save()
        if 'pending_user_type' in request.session:
            del request.session['pending_user_type']
        # Redirect to appropriate dashboard
        if user_type == 'driver':
            return redirect('/driver/')
        else:
            return redirect('/rider/')
    return redirect('/')


def start_social_login(request, role):
    if role not in ['driver', 'rider']:
        return redirect('/')
    request.session['role_intent'] = role
    return redirect('/accounts/google/login/')


@login_required
def login_redirect(request):
    user = request.user

    # Check if user is a moderator
    if user.is_moderator or user.email.lower() in [
        email.lower() for email in getattr(settings, "MODERATOR_EMAILS", [])
    ]:
        if not user.is_moderator:
            user.is_moderator = True
            user.save()
        return redirect('/moderator/')

    # Check if user is verified
    if not user.is_verified:
        return redirect('verification')

    # Check user_type for driver/rider
    if user.user_type == 'driver':
        return redirect('/driver/')
    if user.user_type == 'rider':
        return redirect('/rider/')

    # Fallback
    return redirect('/')

@login_required
def delete_account(request):
    if request.method == 'POST':
        user = request.user
        profile_type = request.POST.get('profile_type')
        
        # Delete only the specific profile type
        if profile_type == 'driver':
            try:
                user.driverprofile.delete()
                messages.success(request, 'Your driver profile has been deleted successfully.')
            except Exception as e:
                messages.error(request, f'Error deleting driver profile: {e}')
        elif profile_type == 'rider':
            try:
                user.riderprofile.delete()
                messages.success(request, 'Your rider profile has been deleted successfully.')
            except Exception as e:
                messages.error(request, f'Error deleting rider profile: {e}')
        
        # Check if user has any remaining profiles
        has_driver = DriverProfile.objects.filter(user=user).exists()
        has_rider = RiderProfile.objects.filter(user=user).exists()
        
        # Update user_type and handle logout
        if not has_driver and not has_rider:
            user.username = "[deleted]"
            user.email = f"deleted_{user.id}@deleted.com"
            user.is_active = False
            user.user_type = None
            user.save()
            logout(request)
            messages.success(request, 'Your account has been completely deleted.')
        else:
            # Update user_type based on remaining profiles
            if profile_type == 'driver' and not has_driver and has_rider:
                user.user_type = 'rider'
            elif profile_type == 'rider' and not has_rider and has_driver:
                user.user_type = 'driver'
            user.save()
            logout(request)
            messages.success(request, f'Your {profile_type} profile has been deleted. Please log in again.')
        
        return redirect('/')
    
    return redirect('/')


@login_required
def verification(request):
    if request.user.is_verified:
        # User is already verified, redirect to appropriate dashboard
        if request.user.user_type == 'driver':
            return redirect('/driver/')
        elif request.user.user_type == 'rider':
            return redirect('/rider/')
        return redirect('/')
    
    if request.method == 'POST':
        student_id = request.POST.get('student_id', '').strip()
        if not student_id:
            messages.error(request, 'Please enter your student ID.')
            return render(request, 'accounts/verification.html')
        
        # Generate verification token
        token = secrets.token_urlsafe(32)
        
        # Save student ID and token to user
        request.user.computing_id = student_id
        request.user.verification_token = token
        request.user.save()
        
        # Send verification email
        email = f"{student_id}@virginia.edu"
        verification_url = request.build_absolute_uri(
            reverse('verify_email', kwargs={'token': token})
        )
        
        subject = 'UVA Rideshare Account Verification'
        message = f'''
Hi,

Please click the link below to verify your UVA Rideshare account:

{verification_url}

If you didn't request this verification, please ignore this email.

Best regards,
UVA Rideshare Team
        '''
        
        try:
            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL if hasattr(settings, 'DEFAULT_FROM_EMAIL') else 'noreply@rideshare.com',
                [email],
                fail_silently=False,
            )
            return render(request, 'accounts/verification.html', {'email_sent': True, 'email': email})
        except Exception as e:
            messages.error(request, 'Failed to send verification email. Please try again.')
    
    return render(request, 'accounts/verification.html')


def verify_email(request, token):
    try:
        user = User.objects.get(verification_token=token)
        user.is_verified = True
        user.verification_token = ''  # Clear the token
        user.save()
        
        if user.user_type == 'driver':
            profile, created = DriverProfile.objects.get_or_create(user=user)
            profile.computing_id = user.computing_id
            if user.first_name and not profile.name:
                profile.name = user.first_name
            profile.save()
        elif user.user_type == 'rider':
            profile, created = RiderProfile.objects.get_or_create(user=user)
            profile.computing_id = user.computing_id
            if user.first_name and not profile.name:
                profile.name = user.first_name
            profile.save()
        
        messages.success(request, 'Your account has been verified successfully!')
        
        # Redirect to appropriate dashboard
        if user.user_type == 'driver':
            return redirect('/driver/')
        elif user.user_type == 'rider':
            return redirect('/rider/')
        
        return redirect('/')
        
    except User.DoesNotExist:
        messages.error(request, 'Invalid verification link.')
        return redirect('/')
