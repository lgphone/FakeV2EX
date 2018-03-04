import re
from django import forms
from django.core.exceptions import ValidationError
from .models import UserProfile


def mobile_validate(value):
    mobile_re = re.compile(r'^(13[0-9]|15[012356789]|17[678]|18[0-9]|14[57])[0-9]{8}$')
    if not mobile_re.match(value):
        raise ValidationError('手机号码格式错误')


def user_unique_validate(username):
    user_obj = UserProfile.objects.filter(username=username).first()
    if user_obj:
        raise ValidationError('此用户名已经存在，请换一个')


def username_rule_validate(value):
    # 先设定一个正则，非 [a-z][0-9]
    username_re = re.compile(r'\W|[A-Z]')
    # 判断如果查找所有的数据后有正则中的指定的字符串
    if username_re.findall(value):
        # 说明匹配，但是匹配就是非[a-z][0-9]  而我们想要的是[a-z][0-9]
        raise ValidationError('用户名格式错误 只能在[a-z][0-9]中选择')
    # 不匹配，说明 value 全在 [a-z][0-9] 这个范围里


def email_unique_validate(email):
    user_obj = UserProfile.objects.filter(email=email).first()
    if user_obj:
        raise ValidationError('Email已经存在，请换一个')


class SignupForm(forms.Form):
    username = forms.CharField(validators=[user_unique_validate, username_rule_validate, ], required=True,
                               max_length=30, min_length=5,
                               error_messages={'required': '用户名不能为空', 'max_length': '用户名至少5位',
                                               'min_length': '用户名最多30位'})
    password = forms.CharField(min_length=6, max_length=50, required=True,
                               error_messages={'required': '密码不能为空',
                                               'invalid': '密码格式错误',
                                               'min_length': '密码不能少于6位',
                                               'max_length': '密码最多50位'})
    email = forms.EmailField(validators=[email_unique_validate, ], required=True,
                             error_messages={'required': '邮箱不能为空', 'invalid': '邮箱格式错误'})
    mobile = forms.CharField(validators=[mobile_validate, ], required=True,
                             error_messages={'required': '手机号不能为空'})


class SigninForm(forms.Form):
    username = forms.CharField(required=True, max_length=50,
                               error_messages={'required': '用户名不能为空'}, )
    password = forms.CharField(min_length=6, max_length=50, required=True,
                               error_messages={'required': '密码不能为空',
                                               'invalid': '密码格式错误',
                                               'min_length': '密码不能少于6位'})
