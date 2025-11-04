from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.conf import settings

class MySocialAccountAdapter(DefaultSocialAccountAdapter):
    def pre_social_login(self, request, sociallogin):
        role = request.session.get('role_intent', None)
        
        if sociallogin.user.pk:  # Existing user
            user = sociallogin.user
            if user.email and user.email.lower() in [e.lower() for e in settings.MODERATOR_EMAILS]:
                user.is_moderator = True
                user.is_staff = True
            else:
                if role in ['driver', 'rider']:
                    user.user_type = role
            user.save()
    
    def save_user(self, request, sociallogin, form=None):
        user = super().save_user(request, sociallogin, form)
        role = request.session.get('role_intent', None)
        
        if user.email and user.email.lower() in [e.lower() for e in settings.MODERATOR_EMAILS]:
            user.is_moderator = True
            user.is_staff = True
        else:
            if role in ['driver', 'rider']:
                user.user_type = role
        
        user.save()
        if 'role_intent' in request.session:
            del request.session['role_intent']
        return user