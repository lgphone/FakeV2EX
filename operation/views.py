import json
from django.shortcuts import render, HttpResponse
from django.views.generic import View
from django.contrib.auth import get_user_model
from django.utils.decorators import method_decorator
from utils.auth_decorator import login_auth
from topic.models import Topic, TopicVote
from .forms import TopicVoteForm
User = get_user_model()
# Create your views here.


class TopicVoteView(View):
    @method_decorator(login_auth)
    def dispatch(self, request, *args, **kwargs):
        return super(TopicVoteView, self).dispatch(request, *args, **kwargs)

    def post(self, request):
        ret = {
            'changed': False,
            'topic_sn': '',
            'data': ''
        }
        user_info = request.session.get('user_info')
        uid = user_info['uid']
        obj = TopicVoteForm(request.POST)
        if obj.is_valid():
            ret['changed'] = True
            topic_sn = obj.cleaned_data['topic_sn']
            print(topic_sn)
            vote_action = obj.cleaned_data['vote_action']
            topic_obj = Topic.objects.filter(topic_sn=topic_sn).first()
            flag = False
            if vote_action == 'up':
                flag = True
            try:
                topic_vote_obj = TopicVote.objects.get(user_id=uid, topic=topic_obj)
                topic_vote_obj.like = flag
                topic_vote_obj.save()
            except TopicVote.DoesNotExist:
                topic_vote_obj = TopicVote()
                topic_vote_obj.user_id = uid
                topic_vote_obj.like = flag
                topic_vote_obj.topic = topic_obj
                topic_vote_obj.save()
            ret['topic_sn'] = topic_sn
            ret['data'] = '''
                <a href="javascript:" onclick="upVoteTopic('{_topic_sn}');" class="vote">
                <li class="fa fa-chevron-up">&nbsp;{_like_num}</li>
                </a> &nbsp;
                <a href="javascript:" onclick="downVoteTopic('{_topic_sn}');" class="vote">
                <li class="fa fa-chevron-down">&nbsp;{_dislike_num}</li>
                </a>
                '''.format(_like_num=topic_vote_obj.count_like(topic_obj),
                           _dislike_num=topic_vote_obj.count_dislike(topic_obj),
                           _topic_sn=topic_sn,)
        else:
            ret['changed'] = False
            ret['data'] = obj.errors.as_json()

        return HttpResponse(json.dumps(ret))
