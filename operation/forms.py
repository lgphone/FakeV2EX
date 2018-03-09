from django import forms
from django.core.exceptions import ValidationError
from topic.models import Topic, TopicCategory


def topic_exist_validate(topic_sn):
    topic_obj = Topic.objects.filter(topic_sn=topic_sn).first()
    if not topic_obj:
        raise ValidationError('Topic 不存在')


def node_exist_validate(node_code):
    node_obj = TopicCategory.objects.filter(code=node_code, category_type=2).first()
    if not node_obj:
        raise ValidationError('Node 不存在')


def vote_action_validate(vote_action):
    allow_action = ['up', 'down']
    if vote_action not in allow_action:
        raise ValidationError('不允许的操作')


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
