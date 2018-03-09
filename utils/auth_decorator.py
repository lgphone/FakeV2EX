from django.shortcuts import redirect
from django.urls import reverse


def login_auth(func):
    def inner(request, *args, **kwargs):
        user_info = request.session.get('user_info', False)
        if not user_info:
            return redirect(reverse('signin') + '?next={_path}'.format(_path=request.path))
        return func(request, *args, **kwargs)
    return inner
