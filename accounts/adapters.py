from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.conf import settings

class MySocialAccountAdapter(DefaultSocialAccountAdapter):
    def save_user(self, request, sociallogin, form=None):
        user = super().save_user(request, sociallogin, form)
        role = request.session.pop('role_intent', None)
        profile = getattr(user, 'profile', None)
        if profile is None:
            from .models import Profile
            profile = Profile.objects.create(user=user)
        if role in ['driver', 'rider']:
            profile.role = role
        if user.email and user.email.lower() in [e.lower() for e in settings.MODERATOR_EMAILS]:
            profile.is_moderator = True
            user.is_staff = True
            user.save()
        profile.save()
        return user