from django.dispatch import receiver
from allauth.socialaccount.signals import pre_social_login
from django.shortcuts import redirect
from django.urls import reverse

from allauth.socialaccount.signals import pre_social_login, social_account_added
from django.contrib.auth.signals import user_logged_in

# @receiver(pre_social_login)
# def handle_social_login(sender, request, sociallogin, **kwargs):
    
#     # Set username from Google data if not set
#     if not sociallogin.user.username and sociallogin.account.extra_data:
#         name = sociallogin.account.extra_data.get('name', '')
#         email = sociallogin.account.extra_data.get('email', '')
#         sociallogin.user.username = name or email.split('@')[0]
    
#     # Determine user type from referrer or session
#     next_url = request.GET.get('next', '')
#     user_type = None
    
#     if '/driver/' in next_url:
#         user_type = 'driver'
#     elif '/rider/' in next_url:
#         user_type = 'rider'
    
#     # Set user type for new users only
#     if user_type and not sociallogin.user.pk:
#         sociallogin.user.user_type = user_type

@receiver(social_account_added)
def set_user_type_on_social_add(sender, request, sociallogin, **kwargs):
    user = sociallogin.user
    if not user.user_type:
        next_url = request.GET.get('next', '')
        if '/driver/' in next_url:
            user.user_type = 'driver'
        elif '/rider/' in next_url:
            user.user_type = 'rider'
        user.save()


@receiver(user_logged_in)
def clear_messages_on_login(sender, request, user, **kwargs):
    # Clear messages on every login to prevent cross-contamination
    if hasattr(request, '_messages'):
        request._messages.used = True