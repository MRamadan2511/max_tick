from functools import wraps
from django.http import HttpResponseForbidden

def user_role_required(allowed_roles=[]):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            user_role = request.user.user_role

            if user_role is None or user_role.role not in allowed_roles:
                return HttpResponseForbidden("You don't have permission to access this page.")

            return view_func(request, *args, **kwargs)

        return _wrapped_view

    return decorator
