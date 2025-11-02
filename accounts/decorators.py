from django.core.exceptions import PermissionDenied

def moderator_required(view_func):
    def _wrapped(request, *args, **kwargs):
        if not request.user.is_authenticated or not getattr(request.user, 'profile', None):
            raise PermissionDenied
        if not request.user.profile.is_moderator:
            raise PermissionDenied
        return view_func(request, *args, **kwargs)
    return _wrapped