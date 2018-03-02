import sys
import os
import json

pwd = os.path.dirname(os.path.realpath(__file__))
sys.path.append(pwd+"../")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "v2ex.settings")

import django
django.setup()
from topic.models import Topic, TopicCategory


tips_obj = Topic.objects.all()

row_data = []

for i in tips_obj:
    tmp = {
        'category': i.category_id,
        'author': i.author_id,
        'tips_sn': i.tips_sn,
        'click_num': i.click_num,
        'like_num': i.like_num,
        'dislike_num': i.dislike_num,
        'title': i.title,
        'content': i.content,
    }
    row_data.append(tmp)
print(row_data)


tips_cate = TopicCategory.objects.all()
tips_data = []
for i in tips_cate:
    tmp = {
        'name': i.name,
        'code': i.code,
        'icon': i.icon,
        'desc': i.desc,
        'category_type': i.category_type,
        'parent_category': i.parent_category_id,
        'is_hot': i.is_hot,
        'avatar': i.avatar
    }
    tips_data.append(tmp)

print(tips_data)