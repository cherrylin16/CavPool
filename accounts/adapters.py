from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.conf import settings

class MySocialAccountAdapter(DefaultSocialAccountAdapter):
    def save_user(self, request, sociallogin, form=None):
        user = super().save_user(request, sociallogin, form)
        role = request.session.pop('role_intent', None)
        
        # Check if user is a moderator first
        if user.email and user.email.lower() in [e.lower() for e in settings.MODERATOR_EMAILS]:
            user.is_moderator = True
            user.is_staff = True
        else:
            # Only set user_type if not a moderator
            if role in ['driver', 'rider']:
                user.user_type = role
        
        user.save()
        return user