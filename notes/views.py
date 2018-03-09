import markdown
from django.shortcuts import render, redirect, HttpResponse
from django.urls import reverse
from django.views.generic import View
from django.contrib.auth import get_user_model
from django.utils.decorators import method_decorator
from utils.auth_decorator import login_auth
from django.http import Http404
from utils.some_utils import gender_topic_sn
from .models import Notes, NotesFolder

User = get_user_model()

exts = ['markdown.extensions.extra', 'markdown.extensions.codehilite', 'markdown.extensions.tables',
        'markdown.extensions.toc']


class NotesView(View):
    @method_decorator(login_auth)
    def dispatch(self, request, *args, **kwargs):
        return super(NotesView, self).dispatch(request, *args, **kwargs)

    def get(self, request, node_code):
        note_obj = Notes.objects.filter(folder_id=1).order_by("-add_time")
        # 去除第一条，第一条是 /
        note_folder_obj = NotesFolder.objects.all().exclude(id=1).order_by("-add_time")
        return render(request, 'note/note.html', locals())



# class NewTopicView(View):
#     @method_decorator(login_auth)
#     def dispatch(self, request, *args, **kwargs):
#         return super(NewTopicView, self).dispatch(request, *args, **kwargs)
#
#     def get(self, request):
#         is_login = request.session.get('isLogin', None)
#         user_info = request.session.get('user_info', None)
#         obj = CheckNodeForm(request.GET)
#         if obj.is_valid():
#             node_code = obj.cleaned_data['node_code']
#             node_obj = TopicCategory.objects.filter(code=node_code, category_type=2).first()
#             return render(request, 'topic/new.html', locals())
#         node_obj = TopicCategory.objects.filter(category_type=2)
#         return render(request, 'topic/new.html', locals())
#
#     def post(self, request):
#         is_login = request.session.get('isLogin', None)
#         user_info = request.session.get('user_info', None)
#         has_error = True
#         obj = NewTopicForm(request.POST)
#         if obj.is_valid():
#             has_error = False
#             username = obj.cleaned_data['username']
#             title = obj.cleaned_data['title']
#             content = obj.cleaned_data['content']
#             node_code = obj.cleaned_data['node_code']
#             topic_sn = gender_topic_sn()
#             if content:
#                 html_content = markdown.markdown(content, format="xhtml5", extensions=exts)
#             else:
#                 html_content = content
#             Topic.objects.create(author=User.objects.filter(username=username).first(), title=title,
#                                  content=content,
#                                  html_content=html_content,
#                                  category=TopicCategory.objects.filter(code=node_code, category_type=2).first(),
#                                  topic_sn=topic_sn)
#             return redirect(reverse('topic', args=(topic_sn,)))
#         node_obj = TopicCategory.objects.filter(category_type=2)
#         return render(request, 'topic/new.html', locals())