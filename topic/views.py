from django.shortcuts import render, redirect
from django.urls import reverse
from django.core.paginator import Paginator
from django.views.generic import View
from django.contrib.auth import get_user_model
from django.utils.decorators import method_decorator
from utils.auth_decorator import login_auth
from django.http import Http404
from utils.some_utils import gender_topic_sn
from .models import TopicCategory, Topic
from .forms import NewTopicForm
User = get_user_model()
# Create your views here.


class IndexView(View):
    def get(self, request):
        is_login = request.session.get('isLogin', None)
        user_info = request.session.get('user_info', None)
        current_tab = request.GET.get('tab', 'tech')
        category_obj = TopicCategory.objects.filter(category_type=1)
        category_children_obj = TopicCategory.objects.filter(parent_category__code=current_tab)
        topic_obj = Topic.objects.filter(category__parent_category__code=current_tab).order_by('add_time')[0:30]
        return render(request, 'topic/index.html', locals())


class NewTopicView(View):
    @method_decorator(login_auth)
    def dispatch(self, request, *args, **kwargs):
        return super(NewTopicView, self).dispatch(request, *args, **kwargs)

    def get(self, request):
        is_login = request.session.get('isLogin', None)
        user_info = request.session.get('user_info', None)
        go_obj = TopicCategory.objects.filter(category_type=2)
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
            go_code = obj.cleaned_data['go_code']
            topic_sn = gender_topic_sn()
            Topic.objects.create(author=User.objects.filter(username=username).first(), title=title, content=content,
                                 category=TopicCategory.objects.filter(code=go_code).first(), topic_sn=topic_sn)
            return redirect(reverse('topic', args=(topic_sn,)))
        go_obj = TopicCategory.objects.filter(category_type=2)
        return render(request, 'topic/new.html', locals())


class RecentView(View):
    def get(self, request):
        is_login = request.session.get('isLogin', None)
        user_info = request.session.get('user_info', None)
        current_page = request.GET.get('p', '1')
        current_page = int(current_page)
        topic_obj = Topic.objects.all().order_by('add_time')[0:30]
        page_obj = Paginator(topic_obj, 15)
        topic_count = page_obj.count
        current_page_obj = page_obj.page(current_page).object_list
        last_page = page_obj.page_range[-1]
        if current_page == 1:
            if len(page_obj.page_range) > 18:
                page_list = list(page_obj.page_range[current_page - 1:10])
            page_list = list(page_obj.page_range)
            print(page_list)
        else:
            if len(page_obj.page_range) > 20:
                page_list = list(page_obj.page_range[:current_page-1][-5])
                page_list += list(page_obj.page_range[current_page-1:5])
            page_list = list(page_obj.page_range)
        return render(request, 'topic/recent.html', locals())


class GoView(View):
    def get(self, request, go_code):
        is_login = request.session.get('isLogin', None)
        user_info = request.session.get('user_info', None)
        current_page = request.GET.get('p', '1')
        current_page = int(current_page)
        go_topic_obj = Topic.objects.filter(category__code=go_code).order_by('id')
        page_obj = Paginator(go_topic_obj, 15)
        topic_count = page_obj.count
        current_page_obj = page_obj.page(current_page).object_list
        last_page = page_obj.page_range[-1]
        if current_page == 1:
            page_list = page_obj.page_range[current_page - 1:10]
        else:
            page_list = list(page_obj.page_range[:current_page - 1][-5])
            page_list += list(page_obj.page_range[current_page - 1:5])
        return render(request, 'topic/go.html', locals())


class GoLinkView(View):
    def get(self, request, go_code):
        is_login = request.session.get('isLogin', None)
        user_info = request.session.get('user_info', None)
        return render(request, 'topic/go_links.html', locals())


class TopicView(View):
    def get(self, request, topic_sn):
        is_login = request.session.get('isLogin', None)
        user_info = request.session.get('user_info', None)
        try:
            topic_obj = Topic.objects.get(topic_sn=topic_sn)
            topic_obj.click_num += 1
            topic_obj.save()
            return render(request, 'topic/topic.html', locals())
        except Topic.DoesNotExist:
            raise Http404("topic does not exist")


