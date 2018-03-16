from django.utils.deprecation import MiddlewareMixin
from django.core.cache import cache
from v2ex.settings import SESSION_COOKIE_AGE
from django.db import connection


class CountOnlineMiddlewareMixin(MiddlewareMixin):

    def process_request(self, request):
        # 获取当前session key
        session_key = request.session.session_key
        # 获取当前访问用户的IP
        if 'HTTP_X_FORWARDED_FOR' in request.META:
            ip = request.META['HTTP_X_FORWARDED_FOR']
        else:
            ip = request.META['REMOTE_ADDR']

        # 判断用户是否登录
        if request.session.get('user_info', False):
            # 因为已经在session中配置了自动更新时间了，下面操作不需要
            # # 在线的话每当用户访问页面要更新session 时间，防止session失效
            # request.session.set_expiry(SESSION_COOKIE_AGE)
            # 统计在线用户，先生成唯一key
            online_key = 'count_online_id_{_id}_session_{_session}'.format(
                _id=request.session.get('user_info')['uid'], _session=session_key)
            # 设置过期时间，或者重新设置过期时间
            cache.set(online_key, 'online', timeout=SESSION_COOKIE_AGE)

        # 把统计数放入请求中，方便在模板中使用
        # 通过通配符获取 count_online 的key 有多少个
        # 如果用户不再看网页，session 和 cache 的key 会自动过期，自动删除
        request.online_member_count = len(cache.keys("count_online_id_*"))
        request.current_visitor_ip = ip

    # 用来查看sql语句的debug 关闭
    # def process_response(self, request, response):
    #     for query in connection.queries:
    #         nice_sql = query['sql'].replace('"', '').replace(',', ', ')
    #         sql = "\033[1;31m[%s]\033[0m %s" % (query['time'], nice_sql)
    #         print(sql)
    #
    #     return response
