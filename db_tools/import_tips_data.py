# -*- coding: utf-8 -*-
__author__ = 'bobby'
import sys
import os


pwd = os.path.dirname(os.path.realpath(__file__))
sys.path.append(pwd+"../")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "v2ex.settings")

import django
django.setup()

from tips.models import Tips

from db_tools.data.tips_data import row_data

for tips_detail in row_data:
    tips = Tips()
    tips.title = tips_detail["title"]
    tips.tips_sn = tips_detail["tips_sn"]
    tips.click_num = tips_detail["click_num"]
    tips.like_num = tips_detail["like_num"]
    tips.dislike_num = tips_detail["dislike_num"]
    tips.title = tips_detail["title"]
    tips.content = tips_detail["content"]
    tips.category = tips_detail["category"]
    tips.author = tips_detail["author"]
    tips.save()
