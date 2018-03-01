import re
from django import forms
from django.core.exceptions import ValidationError


def mobile_validate(value):
    mobile_re = re.compile(r'^(13[0-9]|15[012356789]|17[678]|18[0-9]|14[57])[0-9]{8}$')
    if not mobile_re.match(value):
        raise ValidationError('手机号码格式错误')


class SignupForm(forms.Form):
    username = forms.CharField(required=True, max_length=50,
                               error_messages={'required': '用户名不能为空'},
                               widget=forms.TextInput(attrs={'class': 'sls',
                                                             'name': 'username'}))
    password = forms.CharField(min_length=6, max_length=50, required=True,
                               error_messages={'required': '密码不能为空',
                                               'invalid': '密码格式错误',
                                               'min_length': '密码不能少于6位'})
    email = forms.EmailField(required=True, error_messages={'required': '邮箱不能为空',
                                                            'invalid': '邮箱格式错误'})
    mobile = forms.CharField(validators=[mobile_validate, ], required=True,
                             error_messages={'required': '手机号不能为空'})


class SigninForm(forms.Form):
    username = forms.CharField(required=True, max_length=50,
                               error_messages={'required': '用户名不能为空'},)
    password = forms.CharField(min_length=6, max_length=50, required=True,
                               error_messages={'required': '密码不能为空',
                                               'invalid': '密码格式错误',
                                               'min_length': '密码不能少于6位'})

