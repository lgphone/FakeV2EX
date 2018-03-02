# -*- coding: utf-8 -*-
__author__ = 'bobby'
import sys
import os


pwd = os.path.dirname(os.path.realpath(__file__))
sys.path.append(pwd+"../")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "v2ex.settings")

import django
django.setup()

from topic.models import Topic

from db_tools.data.topic_data import row_data

for tips_detail in row_data:
    tips = Topic()
    tips.title = tips_detail["title"]
    tips.topic_sn = tips_detail["tips_sn"]
    tips.click_num = tips_detail["click_num"]
    tips.like_num = tips_detail["like_num"]
    tips.dislike_num = tips_detail["dislike_num"]
    tips.title = tips_detail["title"]
    tips.content = tips_detail["content"]
    tips.category_id = tips_detail["category"]
    tips.author_id = tips_detail["author"]

    tips.save()
