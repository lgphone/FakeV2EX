from django.shortcuts import render, HttpResponse
from django.core.paginator import Paginator
from django.views.generic import View
from .models import TipsCategory, Tips

# Create your views here.


class IndexView(View):
    def get(self, request):
        current_tab = request.GET.get('tab', 'tech')
        category_obj = TipsCategory.objects.filter(category_type=1)
        category_children_obj = TipsCategory.objects.filter(parent_category__code=current_tab)
        tips_obj = Tips.objects.filter(category__parent_category__code=current_tab).order_by('add_time')[0:30]
        return render(request, 'tips/index.html', locals())


class RecentView(View):
    def get(self, request):
        current_page = request.GET.get('p', '1')
        current_page = int(current_page)
        tips_obj = Tips.objects.all().order_by('add_time')[0:30]
        page_obj = Paginator(tips_obj, 15)
        tips_count = page_obj.count
        current_page_obj = page_obj.page(current_page).object_list
        last_page = page_obj.page_range[-1]
        if current_page == 1:
            page_list = page_obj.page_range[current_page-1:10]
        else:
            page_list = list(page_obj.page_range[:current_page-1][-5])
            page_list += list(page_obj.page_range[current_page-1:5])
        return render(request, 'tips/recent.html', locals())


class GoView(View):
    def get(self, request, code):
        current_page = request.GET.get('p', '1')
        current_page = int(current_page)
        go_tips_obj = Tips.objects.filter(category__code=code).order_by('id')
        page_obj = Paginator(go_tips_obj, 15)
        tips_count = page_obj.count
        current_page_obj = page_obj.page(current_page).object_list
        last_page = page_obj.page_range[-1]
        if current_page == 1:
            page_list = page_obj.page_range[current_page - 1:10]
        else:
            page_list = list(page_obj.page_range[:current_page - 1][-5])
            page_list += list(page_obj.page_range[current_page - 1:5])
        return render(request, 'tips/go.html', locals())


class GoLinkView(View):
    def get(self, request, code):
        return render(request, 'tips/go_links.html', locals())


class TipsView(View):
    def get(self, request, tips_sn):
        tips_obj = Tips.objects.filter(tips_sn=tips_sn).first()
        return render(request, 'tips/tips.html', locals())

