from functools import wraps
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

def verified_required(view_func):
    @wraps(view_func)
    @login_required
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_verified:
            return redirect('verification')
        return view_func(request, *args, **kwargs)
    return _wrapped_view