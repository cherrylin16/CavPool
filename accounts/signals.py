from django.dispatch import receiver
from allauth.socialaccount.signals import pre_social_login
from django.shortcuts import redirect
from django.urls import reverse

@receiver(pre_social_login)
def handle_social_login(sender, request, sociallogin, **kwargs):
    # Check if user_type can be determined from the next URL
    next_url = request.GET.get('next', '')
    user_type = None
    
    if '/driver/' in next_url:
        user_type = 'driver'
    elif '/rider/' in next_url:
        user_type = 'rider'
    
    # Set user type for new users or existing users without type
    if user_type and (not sociallogin.user.pk or not sociallogin.user.user_type):
        sociallogin.user.user_type = user_type