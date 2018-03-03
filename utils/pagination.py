from django.utils.safestring import mark_safe
from v2ex.settings import PRE_PAGE_COUNT, PAGER_NUMS


class Paginator:
    def __init__(self, current_page, data_count, per_page_count=PRE_PAGE_COUNT, pager_num=PAGER_NUMS):
        # 当前页码
        self.current_page = current_page
        # 总数据有多少条
        self.data_count = data_count
        # 每页显示多少数据
        self.per_page_count = per_page_count
        # 显示多少个页码标签
        self.pager_num = pager_num

    # 首页
    @property
    def start(self):
        return (self.current_page - 1) * self.per_page_count

    # 尾页
    @property
    def end(self):
        return self.current_page * self.per_page_count

    # 总页数
    @property
    def total_count(self):
        v, y = divmod(self.data_count, self.per_page_count)
        if y:
            v += 1
        return v

    def page_str(self, base_url):
        # 存放分页的html 数据
        page_list = []
        # 如果数据小于等于每页数据展示的数量，就不显示分页器，直接返回空
        if self.data_count <= self.per_page_count:
            page_str = mark_safe("".join(page_list))
            return page_str

        if self.total_count < self.pager_num:
            start_index = 1
            end_index = self.total_count + 1
        else:
            # 如果当前页码在整个要显示页面的左边
            if self.current_page <= (self.pager_num + 1) / 2:
                start_index = 1
                end_index = self.pager_num + 1
            # 在右边 已经大于页码的一半，需要修改首页页码和尾页页码
            else:
                start_index = self.current_page - (self.pager_num - 1) / 2
                end_index = self.current_page + (self.pager_num + 1) / 2
                if (self.current_page + (self.pager_num - 1) / 2) > self.total_count:
                    end_index = self.total_count + 1
                    start_index = self.total_count - self.pager_num + 1

        # 循环生成页码标签，并添加到list中
        for i in range(int(start_index), int(end_index)):
            if i == self.current_page:
                temp = '<li class="page-item active"><a class="page-link" href="{_base_url}p={_current_page}">{_current_page}</a></li>'.format(
                    _base_url=base_url, _current_page=i)
            else:
                temp = '<li class="page-item"><a class="page-link" href="{_base_url}p={_current_page}">{_current_page}</a></li>'.format(
                    _base_url=base_url, _current_page=i)

            page_list.append(temp)

        # 生成总页数标签,如果总页数比每页数都少，就没必要显示了
        if self.total_count > self.pager_num:
            page_count = '''<li class="page-item disabled">
            <a class="page-link" href="javascript:void(0);">
            <i class="fa fa-ellipsis-h"></i></a></li>
            <li class="page-item">
            <a class="page-link" href="href="{_base_url}p={_total_count}">{_total_count}</a></li>'''.format(
                _base_url=base_url, _total_count=int(self.total_count))

            page_list.append(page_count)

        # 生成跳转按钮
        jump = '''<input type="number" class="page_input" autocomplete="off" value="{_current}" min="1" max="{_max}" onkeydown="if (event.keyCode == 13)
               location.href = '{_base_url}p=' + this.value">'''.format(_base_url=base_url, _current=self.current_page, _max=self.total_count)

        page_list.append(jump)

        # 如果是第一页，禁用上一页按钮
        if self.current_page == 1:
            prev = '<li class="page-item disabled"><a class="page-link" href="javascript:void(0);">上一页</a></li>'
        else:
            prev = '<li class="page-item"><a class="page-link" href="{_base_url}p={_prev_page}">上一页</a></li>'.format(
                _base_url=base_url, _prev_page=self.current_page - 1)

        page_list.append(prev)

        # 如果是最后页，禁用最后页按钮
        if self.current_page == self.total_count:
            nex = '<li class="page-item disabled"><a class="page-link" href="javascript:void(0);">下一页</a></li>'
        else:
            nex = '<li class="page-item"><a class="page-link" href="{_base_url}p={_nex_page}">下一页</a></li>'.format(
                _base_url=base_url, _nex_page=self.current_page + 1)

        page_list.append(nex)

        # 使用Django mark_safe 使得标签可以被原生插入
        page_str = mark_safe("".join(page_list))
        return page_str
