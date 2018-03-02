"""v2ex URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from topic.views import IndexView, GoView, TopicView, GoLinkView, RecentView, NewTopicView
from user.views import SignupView, check_code, SigninView, SignoutView, MemberView
from operation.views import TopicVoteView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', IndexView.as_view(), name='index'),
    path('recent', RecentView.as_view(), name='recent'),
    path('new', NewTopicView.as_view(), name='new'),
    path('member/<slug:username>', MemberView.as_view(), name='member'),
    path('go/<slug:go_code>', GoView.as_view(), name='go'),
    path('go/<slug:go_code>/links', GoLinkView.as_view(), name='go_link'),
    path('t/<slug:topic_sn>', TopicView.as_view(), name='topic'),
    path('topic/vote', TopicVoteView.as_view(), name='topic_vote'),
    path('signup', SignupView.as_view(), name='signup'),
    path('signin', SigninView.as_view(), name='signin'),
    path('signout', SignoutView.as_view(), name='signout'),
    path('check_code', check_code, name='check_code'),
]
