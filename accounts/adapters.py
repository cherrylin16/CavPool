from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.conf import settings

class MySocialAccountAdapter(DefaultSocialAccountAdapter):
    def save_user(self, request, sociallogin, form=None):
        user = super().save_user(request, sociallogin, form)
        role = request.session.pop('role_intent', None)
        
        # Set user_type directly on the User model
        if role in ['driver', 'rider']:
            user.user_type = role
        
        # Check if user is a moderator
        if user.email and user.email.lower() in [e.lower() for e in settings.MODERATOR_EMAILS]:
            user.is_staff = True
        
        user.save()
        return user