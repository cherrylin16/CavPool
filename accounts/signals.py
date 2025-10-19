from django.dispatch import receiver
from allauth.socialaccount.signals import pre_social_login
from django.shortcuts import redirect
from django.urls import reverse

@receiver(pre_social_login)
def handle_social_login(sender, request, sociallogin, **kwargs):
    # Check if user_type is in session from the redirect URL
    next_url = request.GET.get('next', '')
    if 'set-user-type/driver' in next_url:
        request.session['pending_user_type'] = 'driver'
    elif 'set-user-type/rider' in next_url:
        request.session['pending_user_type'] = 'rider'
    
    # If user already exists and has no user_type, set it from session
    if sociallogin.user.pk and not sociallogin.user.user_type:
        user_type = request.session.get('pending_user_type')
        if user_type:
            sociallogin.user.user_type = user_type
            sociallogin.user.save()
            del request.session['pending_user_type']