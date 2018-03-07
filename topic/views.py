import markdown
from django.shortcuts import render, redirect, HttpResponse
from django.urls import reverse
from django.views.generic import View
from django.contrib.auth import get_user_model
from django.utils.decorators import method_decorator
from utils.auth_decorator import login_auth
from django.http import Http404
from utils.some_utils import gender_topic_sn
from utils.pagination import Paginator
from .models import TopicCategory, Topic, NodeLink, Comments
from operation.models import TopicVote, FavoriteNode
from user.models import UserFollowing
from .forms import NewTopicForm, MarkdownPreForm, CheckNodeForm

User = get_user_model()
# Create your views here.

exts = ['markdown.extensions.extra', 'markdown.extensions.codehilite', 'markdown.extensions.tables',
        'markdown.extensions.toc']


class IndexView(View):
    def get(self, request):
        is_login = request.session.get('isLogin', None)
        user_info = request.session.get('user_info', None)
        current_tab = request.GET.get('tab', 'tech')
        category_obj = TopicCategory.objects.filter(category_type=1)
        if current_tab == 'hot':
            category_obj.hot = True
            topic_obj = Topic.objects.all().order_by('-click_num')[0:30]
            return render(request, 'topic/index.html', locals())
        category_children_obj = TopicCategory.objects.filter(parent_category__code=current_tab)
        if current_tab == 'tech':
            topic_obj = Topic.objects.all().order_by('-add_time')[0:30]
        else:
            topic_obj = Topic.objects.filter(category__parent_category__code=current_tab).order_by('-add_time')[0:30]
        return render(request, 'topic/index.html', locals())


class NewTopicView(View):
    @method_decorator(login_auth)
    def dispatch(self, request, *args, **kwargs):
        return super(NewTopicView, self).dispatch(request, *args, **kwargs)

    def get(self, request):
        is_login = request.session.get('isLogin', None)
        user_info = request.session.get('user_info', None)
        obj = CheckNodeForm(request.GET)
        if obj.is_valid():
            node_code = obj.cleaned_data['node_code']
            node_obj = TopicCategory.objects.filter(code=node_code, category_type=2).first()
            return render(request, 'topic/new.html', locals())
        node_obj = TopicCategory.objects.filter(category_type=2)
        return render(request, 'topic/new.html', locals())

    def post(self, request):
        is_login = request.session.get('isLogin', None)
        user_info = request.session.get('user_info', None)
        has_error = True
        obj = NewTopicForm(request.POST)
        if obj.is_valid():
            has_error = False
            username = obj.cleaned_data['username']
            title = obj.cleaned_data['title']
            content = obj.cleaned_data['content']
            node_code = obj.cleaned_data['node_code']
            topic_sn = gender_topic_sn()
            if content:
                html_content = markdown.markdown(content, format="xhtml5", extensions=exts)
            else:
                html_content = content
            Topic.objects.create(author=User.objects.filter(username=username).first(), title=title,
                                 content=content,
                                 html_content=html_content,
                                 category=TopicCategory.objects.filter(code=node_code, category_type=2).first(),
                                 topic_sn=topic_sn)
            return redirect(reverse('topic', args=(topic_sn,)))
        node_obj = TopicCategory.objects.filter(category_type=2)
        return render(request, 'topic/new.html', locals())


class RecentView(View):
    @method_decorator(login_auth)
    def dispatch(self, request, *args, **kwargs):
        return super(RecentView, self).dispatch(request, *args, **kwargs)

    def get(self, request):
        is_login = request.session.get('isLogin', None)
        user_info = request.session.get('user_info', None)
        current_page = request.GET.get('p', '1')
        current_page = int(current_page)
        topic_obj = Topic.objects.all().order_by('-add_time')
        page_obj = Paginator(current_page, topic_obj.count())
        topic_obj = topic_obj[page_obj.start:page_obj.end]
        page_str = page_obj.page_str(reverse('recent') + '?')
        return render(request, 'topic/recent.html', locals())


class NodeView(View):
    def get(self, request, node_code):
        is_login = request.session.get('isLogin', None)
        user_info = request.session.get('user_info', None)
        current_page = request.GET.get('p', '1')
        current_page = int(current_page)
        try:
            node_obj = TopicCategory.objects.get(code=node_code, category_type=2)
            if is_login:
                node_obj.favorite = FavoriteNode.objects.values_list('favorite').filter(user_id=user_info['uid'],
                                                                                        node=node_obj).first()
            topic_obj = Topic.objects.filter(category=node_obj).order_by('-add_time')
            page_obj = Paginator(current_page, topic_obj.count())
            topic_obj = topic_obj[page_obj.start:page_obj.end]
            page_str = page_obj.page_str(reverse('node', args=(node_code,)) + '?')
            return render(request, 'topic/node.html', locals())
        except TopicCategory.DoesNotExist:
            raise Http404("node does not exist")


class NodeLinkView(View):
    def get(self, request, node_code):
        is_login = request.session.get('isLogin', None)
        user_info = request.session.get('user_info', None)
        current_page = request.GET.get('p', '1')
        current_page = int(current_page)
        try:
            node_obj = TopicCategory.objects.get(code=node_code, category_type=2)
            if is_login:
                node_obj.favorite = FavoriteNode.objects.values_list('favorite').filter(user_id=user_info['uid'],
                                                                                        node=node_obj).first()
            node_link_obj = NodeLink.objects.filter(category__code=node_code).order_by('-add_time')
            page_obj = Paginator(current_page, node_link_obj.count())
            node_link_obj = node_link_obj[page_obj.start:page_obj.end]
            page_str = page_obj.page_str(reverse('node_link', args=(node_code,)) + '?')
            return render(request, 'topic/node_link.html', locals())
        except TopicCategory.DoesNotExist:
            raise Http404("node does not exist")


class TopicView(View):
    def get(self, request, topic_sn):
        is_login = request.session.get('isLogin', None)
        user_info = request.session.get('user_info', None)
        try:
            topic_obj = Topic.objects.get(topic_sn=topic_sn)
            topic_obj.click_num += 1
            topic_obj.save()
            topic_obj.like_num = TopicVote.objects.filter(vote=1, topic=topic_obj).count()
            topic_obj.dislike_num = TopicVote.objects.filter(vote=0, topic=topic_obj).count()
            topic_obj.favorite_num = TopicVote.objects.filter(favorite=1, topic=topic_obj).count()
            comments_obj = Comments.objects.filter(topic=topic_obj).select_related('author')
            if is_login:
                topic_obj.thanks = TopicVote.objects.values_list('thanks').filter(topic=topic_obj,
                                                                                  user_id=user_info['uid']).first()
                topic_obj.favorite = TopicVote.objects.values_list('favorite').filter(topic=topic_obj,
                                                                                      user_id=user_info['uid']).first()
            return render(request, 'topic/topic.html', locals())
        except Topic.DoesNotExist:
            raise Http404("topic does not exist")

    @method_decorator(login_auth)
    def post(self, request, topic_sn):
        user_info = request.session.get('user_info', None)
        content = request.POST.get('content', None)
        if content is not None:
            try:
                topic_obj = Topic.objects.get(topic_sn=topic_sn)
                Comments.objects.create(topic=topic_obj, author_id=user_info['uid'], content=content)
                return redirect(reverse('topic', args=(topic_sn,)))
            except Topic.DoesNotExist:
                raise Http404("topic does not exist")


class MarkdownPreView(View):
    @method_decorator(login_auth)
    def dispatch(self, request, *args, **kwargs):
        return super(MarkdownPreView, self).dispatch(request, *args, **kwargs)

    def post(self, request):
        obj = MarkdownPreForm(request.POST)
        if obj.is_valid():
            md = obj.cleaned_data['md']
            md_html = markdown.markdown(md, format="xhtml5", extensions=exts)
            return HttpResponse(md_html)

        return HttpResponse('')


class MyFavoriteNodeView(View):
    @method_decorator(login_auth)
    def dispatch(self, request, *args, **kwargs):
        return super(MyFavoriteNodeView, self).dispatch(request, *args, **kwargs)

    def get(self, request):
        is_login = request.session.get('isLogin', None)
        user_info = request.session.get('user_info', None)
        my_favorite_obj = FavoriteNode.objects.filter(favorite=1, user_id=user_info['uid']).select_related(
            'node').order_by('-add_time')
        return render(request, 'topic/my_node.html', locals())


class MyFavoriteTopicView(View):
    @method_decorator(login_auth)
    def dispatch(self, request, *args, **kwargs):
        return super(MyFavoriteTopicView, self).dispatch(request, *args, **kwargs)

    def get(self, request):
        is_login = request.session.get('isLogin', None)
        user_info = request.session.get('user_info', None)
        my_favorite_obj = TopicVote.objects.filter(favorite=1,
                                                   user_id=user_info['uid']).select_related('topic__author',
                                                                                            'topic__category').order_by(
            '-add_time')
        return render(request, 'topic/my_topic.html', locals())


class MyFollowingView(View):
    @method_decorator(login_auth)
    def dispatch(self, request, *args, **kwargs):
        return super(MyFollowingView, self).dispatch(request, *args, **kwargs)

    def get(self, request):
        is_login = request.session.get('isLogin', None)
        user_info = request.session.get('user_info', None)
        # 获取当前我正在关注的用户的QuerySet  判断 is_following  是不是 1
        my_following_obj = UserFollowing.objects.filter(user_id=user_info['uid'], is_following=1).select_related(
            'following')
        print(my_following_obj)
        # 设定一个列表，存放查询到的所收藏的用户的id
        following_user_id = []
        # 把id 加入列表
        for obj in my_following_obj:
            following_user_id.append(obj.following.id)
        # 查询用户id在所关注的用户的主题
        following_topic_obj = Topic.objects.filter(author_id__in=following_user_id).select_related('category',
                                                                                                   'author').order_by(
            '-add_time')
        return render(request, 'topic/my_following.html', locals())
