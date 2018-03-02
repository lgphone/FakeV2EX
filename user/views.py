from io import BytesIO
import time
from django.shortcuts import render, HttpResponse, redirect
from django.views.generic import View
from django.db.models import Q
from utils.check_code import create_validate_code
from .models import UserProfile
from .forms import SignupForm, SigninForm
# Create your views here.


def check_code(request):
    """
    验证码
    :param request:
    :return:
    """
    stream = BytesIO()
    img, code = create_validate_code()
    img.save(stream, 'PNG')
    request.session['CheckCode'] = code
    return HttpResponse(stream.getvalue())


class SignupView(View):
    def get(self, request):
        return render(request, 'user/signup.html')

    def post(self, request):
        has_error = True
        if request.POST.get('check_code', None):
            if request.session['CheckCode'].upper() == request.POST.get('check_code').upper():
                obj = SignupForm(request.POST)
                if obj.is_valid():
                    has_error = False
                    username = obj.cleaned_data['username']
                    password = obj.cleaned_data['password']
                    email = obj.cleaned_data['email']
                    mobile = obj.cleaned_data['mobile']
                    user_obj = UserProfile()
                    user_obj.username = username
                    user_obj.email = email
                    user_obj.mobile = mobile
                    user_obj.set_password(password)
                    user_obj.save()
                    return redirect('/signin')
            else:
                code_error = "验证码错误"
        else:
            code_error = "请输入验证码"
        return render(request, 'user/signup.html', locals())


class SigninView(View):
    def get(self, request):
        return render(request, 'user/signin.html')

    def post(self, request):
        has_error = True
        if request.POST.get('check_code', None):
            if request.session['CheckCode'].upper() == request.POST.get('check_code').upper():
                obj = SigninForm(request.POST)
                if obj.is_valid():
                    username = obj.cleaned_data['username']
                    password = obj.cleaned_data['password']
                    user_obj = UserProfile.objects.filter(Q(username=username) | Q(email=username)).first()
                    if user_obj:
                        if user_obj.check_password(password):
                            current_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                            user_obj.last_login = current_time
                            user_obj.save()
                            user_info = {
                                'username': username,
                                'avatar': user_obj.avatar,
                                'mobile': user_obj.mobile,
                            }
                            resp = redirect('/')
                            request.session['isLogin'] = True
                            request.session['user_info'] = user_info
                            return resp
                        else:
                            user_error = '用户或密码错误'
                    else:
                        user_error = '用户不存在'
            else:
                code_error = "验证码错误"
        else:
            code_error = "请输入验证码"
        return render(request, 'user/signin.html', locals())


class SignoutView(View):
    def get(self, request):
        request.session['isLogin'] = False
        resp = render(request, 'user/signout.html')
        return resp


class MemberView(View):
    def get(self, request, username):
        is_login = request.session.get('isLogin', None)
        user_info = request.session.get('user_info', None)
        user_obj = UserProfile.objects.filter(username=username).first()
        return render(request, 'user/member.html', locals())
