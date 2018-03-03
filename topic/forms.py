from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from topic.models import TopicCategory
User = get_user_model()


def user_validate(username):
        if not User.objects.filter(username=username).first():
            raise ValidationError('用户不存在')


def node_validate(node_code):
    if not TopicCategory.objects.filter(code=node_code, category_type=2).first():
        raise ValidationError('标签不存在')


class NewTopicForm(forms.Form):
    username = forms.CharField(validators=[user_validate, ], required=True,
                               max_length=50, error_messages={'required': '用户不存在'},)
    title = forms.CharField(max_length=120, required=True,
                            error_messages={'required': '标题不能为空', 'max_length': '超过标题字符限定'})
    content = forms.CharField(max_length=20000, required=False,
                              error_messages={'max_length': '超过内容字符限定'})
    node_code = forms.CharField(validators=[node_validate, ], required=True,
                                error_messages={'required': '标签不能为空'})


class CheckNodeForm(forms.Form):
    node_code = forms.CharField(validators=[node_validate, ], required=True,
                                error_messages={'required': '标签不能为空'})


class MarkdownPreForm(forms.Form):
    md = forms.CharField(max_length=20000, required=True,
                         error_messages={'required': '内容不能为空', 'max_length': '超过字符限定'})
