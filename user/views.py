from io import BytesIO
import time
from django.shortcuts import render, HttpResponse, redirect
from django.urls import reverse
from django.views.generic import View
from django.http import Http404
from django.db.models import Q
from utils.check_code import create_validate_code
from .models import UserProfile, UserFollowing
from operation.models import TopicVote, FavoriteNode, Topic
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
                    return redirect(reverse('signin'))
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
                            user_obj.status = 'ONLINE'
                            user_obj.save()
                            user_info = {
                                'username': username,
                                'uid': user_obj.id,
                                'avatar': user_obj.avatar,
                                'mobile': user_obj.mobile,
                                'favorite_node_num': FavoriteNode.objects.filter(favorite=1, user=user_obj).count(),
                                'favorite_topic_num': TopicVote.objects.filter(favorite=1, user=user_obj).count(),
                                'following_user_num': UserFollowing.objects.filter(is_following=1, user=user_obj).count()
                            }
                            resp = redirect(reverse('index'))
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
        user_info = request.session.get('user_info', None)
        if user_info:
            request.session['isLogin'] = False
            del request.session['user_info']
            user_obj = UserProfile.objects.filter(id=user_info['uid']).first()
            if user_obj:
                user_obj.status = 'OFFLINE'
        return render(request, 'user/signout.html')


class MemberView(View):
    def get(self, request, username):
        # 判断是否是登录用户，调整页面显示按钮
        is_login = request.session.get('isLogin', None)
        # 从session中获取当前用户信息
        user_info = request.session.get('user_info', None)
        try:
            # 获取链接指向的用户名的obj
            user_obj = UserProfile.objects.get(username=username)
            # 获取作者是连接中的用户的Topic主题
            topic_obj = Topic.objects.filter(author=user_obj).select_related('category')
            if is_login:
                # 获取当前用户是否following 此用户 根据此来调整页面显示信息
                is_following = UserFollowing.objects.values_list('is_following').filter(is_following=1,
                                                                                        user_id=user_info['uid'],
                                                                                        following=user_obj).first()
                # 获取当前用户是否block 此用户
                is_block = UserFollowing.objects.values_list('is_block').filter(is_block=1, user_id=user_info['uid'],
                                                                                following=user_obj).first()
            # print(is_following)
            # print(is_block)
            return render(request, 'user/member.html', locals())
        # 没有此用户，指向没有的连接，返回404
        except UserProfile.DoesNotExist:
            raise Http404("Not Find This User")
