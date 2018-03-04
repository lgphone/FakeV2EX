import json
from django.shortcuts import HttpResponse, redirect
from django.urls import reverse
from django.http import Http404
from django.views.generic import View
from django.utils.decorators import method_decorator
from utils.auth_decorator import login_auth
from django.contrib.auth import get_user_model
from .models import Topic, TopicVote, FavoriteNode, TopicCategory
from .forms import TopicVoteForm, CheckTopicForm, CheckNodeForm
from user.models import UserFollowing

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
            flag = 0
            if vote_action == 'up':
                flag = 1
            try:
                topic_vote_obj = TopicVote.objects.get(user_id=uid, topic=topic_obj)
                topic_vote_obj.vote = flag
                topic_vote_obj.save()
            except TopicVote.DoesNotExist:
                topic_vote_obj = TopicVote()
                topic_vote_obj.user_id = uid
                topic_vote_obj.vote = flag
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


class FavoriteTopicView(View):
    @method_decorator(login_auth)
    def dispatch(self, request, *args, **kwargs):
        return super(FavoriteTopicView, self).dispatch(request, *args, **kwargs)

    def post(self, request):
        ret = {
            'changed': False,
            'topic_sn': '',
            'data': ''
        }
        user_info = request.session.get('user_info')
        uid = user_info['uid']
        obj = CheckTopicForm(request.POST)
        if obj.is_valid():
            ret['changed'] = True
            topic_sn = obj.cleaned_data['topic_sn']
            topic_obj = Topic.objects.filter(topic_sn=topic_sn).first()
            try:
                topic_vote_obj = TopicVote.objects.get(user_id=uid, topic=topic_obj)
                if topic_vote_obj.favorite == 1:
                    topic_vote_obj.favorite = 0
                    user_info['favorite_topic_num'] -= 1
                    ret['data'] = "&nbsp;加入收藏&nbsp;"
                else:
                    topic_vote_obj.favorite = 1
                    user_info['favorite_topic_num'] += 1
                    ret['data'] = "&nbsp;取消收藏&nbsp;"
                topic_vote_obj.save()
            except TopicVote.DoesNotExist:
                topic_vote_obj = TopicVote()
                topic_vote_obj.user_id = uid
                topic_vote_obj.favorite = 1
                topic_vote_obj.topic = topic_obj
                topic_vote_obj.save()
                user_info['favorite_topic_num'] += 1
                ret['data'] = "&nbsp;取消收藏&nbsp;"
            request.session['user_info'] = user_info
            ret['topic_sn'] = topic_sn
        else:
            ret['changed'] = False
            ret['data'] = obj.errors.as_json()

        return HttpResponse(json.dumps(ret))


class ThanksTopicView(View):
    @method_decorator(login_auth)
    def dispatch(self, request, *args, **kwargs):
        return super(ThanksTopicView, self).dispatch(request, *args, **kwargs)

    def post(self, request):
        ret = {
            'changed': False,
            'topic_sn': '',
            'data': ''
        }
        user_info = request.session.get('user_info')
        uid = user_info['uid']
        obj = CheckTopicForm(request.POST)
        if obj.is_valid():
            ret['changed'] = True
            topic_sn = obj.cleaned_data['topic_sn']
            topic_obj = Topic.objects.filter(topic_sn=topic_sn).first()
            try:
                topic_vote_obj = TopicVote.objects.get(user_id=uid, topic=topic_obj)
                print(topic_vote_obj)
                if topic_vote_obj.thanks == 1:
                    ret['changed'] = False
                else:
                    topic_vote_obj.thanks = 1
                    topic_vote_obj.save()
            except TopicVote.DoesNotExist:
                topic_vote_obj = TopicVote()
                topic_vote_obj.user_id = uid
                topic_vote_obj.thanks = 1
                topic_vote_obj.topic = topic_obj
                topic_vote_obj.save()
                '''
                等待添加功能，联合查询此贴作者并修改金币数量，添加，并把此感谢者金币减少
                '''
            ret['data'] = "&nbsp;已经发送感谢&nbsp;"
            ret['topic_sn'] = topic_sn
        else:
            ret['changed'] = False
            ret['data'] = obj.errors.as_json()

        return HttpResponse(json.dumps(ret))


class FavoriteNodeView(View):
    @method_decorator(login_auth)
    def dispatch(self, request, *args, **kwargs):
        return super(FavoriteNodeView, self).dispatch(request, *args, **kwargs)

    def post(self, request):
        ret = {
            'changed': False,
            'node_code': '',
            'data': ''
        }
        user_info = request.session.get('user_info')
        uid = user_info['uid']
        obj = CheckNodeForm(request.POST)
        if obj.is_valid():
            ret['changed'] = True
            node_code = obj.cleaned_data['node_code']
            node_obj = TopicCategory.objects.filter(code=node_code, category_type=2).first()
            try:
                favorite_node_obj = FavoriteNode.objects.get(user_id=uid, node=node_obj)
                if favorite_node_obj.favorite == 1:
                    favorite_node_obj.favorite = 0
                    user_info['favorite_node_num'] -= 1
                    ret['data'] = "加入收藏"
                else:
                    favorite_node_obj.favorite = 1
                    user_info['favorite_node_num'] += 1
                    ret['data'] = "取消收藏"
                favorite_node_obj.save()
            except FavoriteNode.DoesNotExist:
                favorite_node_obj = FavoriteNode()
                favorite_node_obj.user_id = uid
                favorite_node_obj.favorite = 1
                favorite_node_obj.node = node_obj
                favorite_node_obj.save()
                user_info['favorite_node_num'] += 1
                ret['data'] = "取消收藏"
            request.session['user_info'] = user_info
            ret['node_code'] = node_code
        else:
            ret['changed'] = False
            ret['data'] = obj.errors.as_json()

        return HttpResponse(json.dumps(ret))


class FollowingView(View):
    @method_decorator(login_auth)
    def dispatch(self, request, *args, **kwargs):
        return super(FollowingView, self).dispatch(request, *args, **kwargs)

    def get(self, request, username):
        user_info = request.session.get('user_info')
        if username == user_info['username']:
            return redirect(reverse('member', args=(username,)))
        following_user_obj = User.objects.filter(username=username).first()
        if following_user_obj:
            try:
                following_obj = UserFollowing.objects.get(user_id=user_info['uid'], following=following_user_obj)
                if following_obj.is_following == 1:
                    following_obj.is_following = 0
                    user_info['following_user_num'] -= 1
                else:
                    following_obj.is_following = 1
                    user_info['following_user_num'] += 1
                following_obj.save()
            except UserFollowing.DoesNotExist:
                following_obj = UserFollowing()
                following_obj.user_id = user_info['uid']
                following_obj.is_following = 1
                following_obj.following = following_user_obj
                following_obj.save()
                user_info['following_user_num'] += 1
            request.session['user_info'] = user_info
            return redirect(reverse('member', args=(username,)))
        else:
            raise Http404("will following user does not exist")


class BlockView(View):
    @method_decorator(login_auth)
    def dispatch(self, request, *args, **kwargs):
        return super(BlockView, self).dispatch(request, *args, **kwargs)

    def get(self, request, username):
        user_info = request.session.get('user_info')
        if username == user_info['username']:
            return redirect(reverse('member', args=(username,)))
        block_user_obj = User.objects.filter(username=username).first()
        if block_user_obj:
            try:
                block_obj = UserFollowing.objects.get(user_id=user_info['uid'], following=block_user_obj)
                if block_obj.is_block == 1:
                    block_obj.is_block = 0
                else:
                    block_obj.is_block = 1
                block_obj.save()
            except UserFollowing.DoesNotExist:
                block_obj = FavoriteNode()
                block_obj.user_id = user_info['uid']
                block_obj.is_block = 1
                block_obj.following = block_user_obj
                block_obj.save()
            return redirect(reverse('member', args=(username,)))
        else:
            raise Http404("will block user does not exist")
