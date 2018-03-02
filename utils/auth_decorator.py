from django.shortcuts import redirect


def login_auth(func):
    def inner(request, *args, **kwargs):
        session_id = request.session.get('isLogin', False)
        if not session_id:
            return redirect('/signin')
        return func(request, *args, **kwargs)
    return inner
