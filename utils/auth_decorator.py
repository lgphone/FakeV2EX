from django.shortcuts import redirect
from django.urls import reverse


def login_auth(func):
    def inner(request, *args, **kwargs):
        session_id = request.session.get('isLogin', False)
        if not session_id:
            return redirect(reverse('signin') + '?next={_path}'.format(_path=request.path))
        return func(request, *args, **kwargs)
    return inner
