import re
from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from topic.models import Topic, TopicCategory

User = get_user_model()


def topic_exist_validate(topic_sn):
    topic_obj = Topic.objects.filter(topic_sn=topic_sn).first()
    if not topic_obj:
        raise ValidationError('Topic 不存在')


def email_unique_validate(email):
    user_obj = User.objects.filter(email=email).first()
    if user_obj:
        raise ValidationError('Email已经存在，请换一个')


def node_exist_validate(node_code):
    node_obj = TopicCategory.objects.filter(code=node_code, category_type=2).first()
    if not node_obj:
        raise ValidationError('Node 不存在')


def vote_action_validate(vote_action):
    allow_action = ['up', 'down']
    if vote_action not in allow_action:
        raise ValidationError('不允许的操作')


def mobile_validate(value):
    mobile_re = re.compile(r'^(13[0-9]|15[012356789]|17[678]|18[0-9]|14[57])[0-9]{8}$')
    if not mobile_re.match(value):
        raise ValidationError('手机号码格式错误')


class TopicVoteForm(forms.Form):
    vote_action = forms.CharField(validators=[vote_action_validate, ], required=True,
                                  error_messages={'required': 'vote_action 不能为空'})
    topic_sn = forms.CharField(validators=[topic_exist_validate, ], required=True,
                               error_messages={'required': 'topic_sn 不能为空'})


class CheckTopicForm(forms.Form):
    topic_sn = forms.CharField(validators=[topic_exist_validate, ], required=True,
                               error_messages={'required': 'topic_sn 不能为空'})


class CheckNodeForm(forms.Form):
    node_code = forms.CharField(validators=[node_exist_validate, ], required=True,
                                error_messages={'required': 'node_code 不能为空'})


class SettingsForm(forms.Form):
    website = forms.CharField(required=False, max_length=50, error_messages={'max_length': '最多50位'})
    company = forms.CharField(required=False, max_length=50, error_messages={'max_length': '最多50位'})
    company_title = forms.CharField(required=False, max_length=50, error_messages={'max_length': '最多50位'})
    location = forms.CharField(required=False, max_length=11, error_messages={'max_length': '最多11位'})
    bio = forms.CharField(required=False, max_length=50, error_messages={'max_length': '最多50位'})
    list_rich = forms.CharField(required=False, max_length=2, error_messages={'max_length': '最多2位'})
    show_balance = forms.CharField(required=False, max_length=2, error_messages={'max_length': '最多2位'})
    my_home = forms.CharField(required=False, max_length=50, error_messages={'max_length': '最多50位'})


class PhoneSettingsForm(forms.Form):
    new_phone_number = forms.CharField(validators=[mobile_validate, ], required=True,
                                       error_messages={'required': '手机号不能为空'})
    password = forms.CharField(required=True, error_messages={'required': '密码不能为空'})


class EmailSettingsForm(forms.Form):
    new_email = forms.EmailField(validators=[email_unique_validate, ], required=True,
                                 error_messages={'required': '邮箱不能为空',
                                                 'invalid': '无效的邮箱地址'})
    password = forms.CharField(required=True, error_messages={'required': '密码不能为空'})


class AvatarSettingsForm(forms.Form):
    avatar = forms.ImageField(error_messages={'required': '文件不能为空',
                                              'invalid': '无效的头像图片'})


class PasswordSettingsForm(forms.Form):
    password_new = forms.CharField(min_length=6, max_length=50, required=True,
                                   error_messages={'required': '新密码不能为空',
                                                   'invalid': '新密码格式错误',
                                                   'min_length': '新密码不能少于6位'})
    password_again = forms.CharField(min_length=6, max_length=50, required=True,
                                     error_messages={'required': '第二次密码不能为空',
                                                     'invalid': '第二次密码格式错误',
                                                     'min_length': '第二次密码不能少于6位'})
    password_current = forms.CharField(min_length=6, max_length=50, required=True,
                                       error_messages={'required': '当前密码不能为空',
                                                       'invalid': '当前密码格式错误',
                                                       'min_length': '当前密码不能少于6位'})
