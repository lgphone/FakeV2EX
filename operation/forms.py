from django import forms
from django.core.exceptions import ValidationError
from topic.models import Topic


def topic_exist_validate(topic_sn):
    topic_obj = Topic.objects.filter(topic_sn=topic_sn).first()
    if not topic_obj:
        raise ValidationError('Topic 不存在')


def vote_action_validate(vote_action):
    allow_action = ['up', 'down']
    if vote_action not in allow_action:
        raise ValidationError('不允许的操作')


class TopicVoteForm(forms.Form):
    vote_action = forms.CharField(validators=[vote_action_validate, ], required=True,
                                  error_messages={'required': 'vote_action 不能为空'})
    topic_sn = forms.CharField(validators=[topic_exist_validate, ], required=True,
                               error_messages={'required': 'topic_sn 不能为空'})
