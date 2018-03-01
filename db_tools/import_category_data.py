# -*- coding: utf-8 -*-
__author__ = 'bobby'

#独立使用django的model
import sys
import os


pwd = os.path.dirname(os.path.realpath(__file__))
sys.path.append(pwd+"../")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "v2ex.settings")

import django
django.setup()

from tips.models import TipsCategory

from db_tools.data.category_data import row_data

for i in row_data:
    i_obj = TipsCategory()
    i_obj.code = i["code"]
    i_obj.name = i["name"]
    i_obj.desc = i["desc"]
    i_obj.category_type = i["category_type"]
    i_obj.parent_category = i["parent_category"]
    i_obj.is_hot = i["is_hot"]
    i_obj.avatar = i["avatar"]
    i_obj.save()
