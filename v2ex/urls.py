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
from topic.views import IndexView, NodeView, TopicView, NodeLinkView, RecentView, NewTopicView, MarkdownPreView, \
    MyFavoriteNodeView, MyFavoriteTopicView, MyFollowingView
from user.views import SignupView, check_code, SigninView, SignoutView, MemberView
from operation.views import TopicVoteView, FavoriteTopicView, ThanksTopicView, FavoriteNodeView, FollowingView, \
    BlockView, SettingView, PhoneSettingView, EmailSettingView, SendActivateCodeView, ActivateEmailView,\
    AvatarSettingView, PasswordSettingView, DailyMissionView, DailyRandomBalanceView, BalanceView

urlpatterns = [
    # 管理员
    path('admin/', admin.site.urls),
    # 首页，默认是最热节点 最多30条
    path('', IndexView.as_view(), name='index'),
    # re_path(r'^$', IndexView.as_view(), name='index'),
    # 所有主题，按最新时间排序
    path('recent', RecentView.as_view(), name='recent'),
    # 发布新主题
    path('new', NewTopicView.as_view(), name='new'),
    # notes
    # path('n', NewTopicView.as_view(), name='new'),
    # 查看某个用户信息
    path('member/<slug:username>', MemberView.as_view(), name='member'),
    # 到某个节点下的主题
    path('go/<slug:node_code>', NodeView.as_view(), name='node'),
    # 到某个节点下的实用节点链接
    path('go/<slug:node_code>/links', NodeLinkView.as_view(), name='node_link'),
    # 主题查看
    path('t/<slug:topic_sn>', TopicView.as_view(), name='topic'),
    # 主题投票
    path('topic/vote', TopicVoteView.as_view(), name='topic_vote'),
    # 主题收藏
    path('topic/favorite', FavoriteTopicView.as_view(), name='favorite_topic'),
    # 主题感谢
    path('topic/thanks', ThanksTopicView.as_view(), name='thanks_topic'),
    # 节点收藏
    path('node/favorite', FavoriteNodeView.as_view(), name='favorite_node'),
    # 用户注册
    path('signup', SignupView.as_view(), name='signup'),
    # 用户登录
    path('signin', SigninView.as_view(), name='signin'),
    # 用户退出
    path('signout', SignoutView.as_view(), name='signout'),
    # 用户设置
    path('settings', SettingView.as_view(), name='settings'),
    # 用户头像设置
    path('settings/avatar', AvatarSettingView.as_view(), name='settings_avatar'),
    # 用户手机设置
    path('settings/phone', PhoneSettingView.as_view(), name='settings_phone'),
    # 用户Email设置
    path('settings/email', EmailSettingView.as_view(), name='settings_email'),
    # 密码修改
    path('settings/password', PasswordSettingView.as_view(), name='settings_password'),
    # 发送随机码地址
    path('activate', SendActivateCodeView.as_view(), name='activate'),
    # 用户邮箱激活链接
    path('activate/<slug:code>', ActivateEmailView.as_view(), name='activate_email'),
    # Following 动作
    path('following/<slug:username>', FollowingView.as_view(), name='following'),
    # Block 动作
    path('block/<slug:username>', BlockView.as_view(), name='block'),
    # 我收藏的节点
    path('my/nodes', MyFavoriteNodeView.as_view(), name='my_nodes'),
    # 我收藏的主题
    path('my/topics', MyFavoriteTopicView.as_view(), name='my_topics'),
    # 我关注的人的信息
    path('my/following', MyFollowingView.as_view(), name='my_following'),
    # 生成图形验证码
    path('check_code', check_code, name='check_code'),
    # 发帖时markdown 格式预览
    path('preview/markdown', MarkdownPreView.as_view(), name='markdown_preview'),
    # 每日金币奖励
    path('mission/daily', DailyMissionView.as_view(), name='daily_mission'),
    # 随机生成金钱接口
    path('mission/daily/redeem', DailyRandomBalanceView.as_view(), name='daily_random_balance'),
    # 用户金钱
    path('balance', BalanceView.as_view(), name='balance'),
]
