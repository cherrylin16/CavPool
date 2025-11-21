from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from django.conf import settings

class MySocialAccountAdapter(DefaultSocialAccountAdapter):
    def populate_username(self, request, user):
        if hasattr(user, 'socialaccount_set'):
            for account in user.socialaccount_set.all():
                if account.provider == 'google' and account.extra_data.get('email'):
                    return account.extra_data['email']
        return super().populate_username(request, user)
    
    def pre_social_login(self, request, sociallogin):
        role = request.session.get('role_intent', None)
        
        if sociallogin.user.pk:  # Existing user
            user = sociallogin.user
            
            if sociallogin.account.extra_data.get('name'):
                full_name = sociallogin.account.extra_data['name'].title()
                user.first_name = full_name
            
            if user.email and user.email.lower() in [e.lower() for e in settings.MODERATOR_EMAILS]:
                user.is_moderator = True
                user.is_staff = True
            else:
                if role in ['driver', 'rider']:
                    user.user_type = role
                    # Store login type for verification redirect
                    request.session['login_type'] = role
            user.save()
    
    def save_user(self, request, sociallogin, form=None):
        if sociallogin.account.extra_data.get('email'):
            sociallogin.user.username = sociallogin.account.extra_data['email']
        
        user = super().save_user(request, sociallogin, form)
        role = request.session.get('role_intent', None)
        
        if sociallogin.account.extra_data.get('name'):
            user.first_name = sociallogin.account.extra_data['name'].title()
        
        if user.email and user.email.lower() in [e.lower() for e in settings.MODERATOR_EMAILS]:
            user.is_moderator = True
            user.is_staff = True
        else:
            if role in ['driver', 'rider']:
                user.user_type = role
                # Store login type for verification redirect
                request.session['login_type'] = role
        
        user.save()
        if 'role_intent' in request.session:
            del request.session['role_intent']
        return user