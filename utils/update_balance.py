from django.contrib.sessions.backends.cache import SessionStore
from django.db.models import F
from django.urls import reverse
from operation.models import BalanceInfo, UserDetails


def update_balance(request, update_type, obj=None):
    # 创建主题
    if update_type == 'create':
        # 获取当前用户的id
        uid = request.session.get('user_info')['uid']
        # 设置改变值
        change_balance = -20
        # 类型
        balance_type = "创建主题"
        # 描述
        marks = '创建了的主题 > <a href="{_uri}">{_title}</a>'.format(_uri=reverse('topic', args=(obj.topic_sn,)),
                                                                _title=obj.title)

        # 更新数据库中的用户余额
        UserDetails.objects.filter(user_id=uid).update(balance=F('balance') + change_balance)

        # 获取此用户更新后的balance
        user_obj = UserDetails.objects.filter(user_id=uid).first()

        # 创建余额变动清单
        BalanceInfo.objects.create(
            user_id=uid,
            balance_type=balance_type,
            balance=change_balance,
            marks=marks,
            last_balance=user_obj.balance
        )

        # 更新session 中数据
        request.session['user_info']['balance'] = user_obj.balance

    # 创建回复
    elif update_type == 'reply':
        uid = request.session.get('user_info')['uid']
        change_balance = -5
        balance_type = "创建回复"
        marks = '在主题 > <a href="{_uri}">{_title}</a> 中创建了回复'.format(_uri=reverse('topic', args=(obj.topic_sn,)),
                                                                    _title=obj.title)

        # 更新数据库中的用户余额
        UserDetails.objects.filter(user_id=uid).update(balance=F('balance') + change_balance)

        # 获取此用户更新后的balance
        user_obj = UserDetails.objects.filter(user_id=uid).first()

        # 创建余额变动清单
        BalanceInfo.objects.create(
            user_id=uid,
            balance_type=balance_type,
            balance=change_balance,
            marks=marks,
            last_balance=user_obj.balance
        )

        # 更新session 中数据
        request.session['user_info']['balance'] = user_obj.balance

    # 感谢主题
    elif update_type == 'thanks':
        uid = request.session.get('user_info')['uid']
        change_balance = -15
        balance_type = "发送谢意"
        marks = '感谢 <a href="{_member_uri}">{_author}</a> 的 > <a href="{_uri}">{_title}</a> 主题'.format(
            _member_uri=reverse('member', args=(obj.author.username,)), _author=obj.author.username,
            _uri=reverse('topic', args=(obj.topic_sn,)), _title=obj.title)

        # 更新数据库中的用户余额
        UserDetails.objects.filter(user_id=uid).update(balance=F('balance') + change_balance)

        # 获取此用户更新后的balance
        user_obj = UserDetails.objects.filter(user_id=uid).first()

        # 创建余额变动清单
        BalanceInfo.objects.create(
            user_id=uid,
            balance_type=balance_type,
            balance=change_balance,
            marks=marks,
            last_balance=user_obj.balance
        )

        # 更新session 中数据
        request.session['user_info']['balance'] = user_obj.balance

    # 收到感谢
    elif update_type == 'recv_thanks':
        # 获取基础信息
        uid = obj.author_id
        change_balance = 10
        balance_type = "收到谢意"
        marks = '主题 > <a href="{_uri}">{_title}</a> 收到感谢'.format(_uri=reverse('topic', args=(obj.topic_sn,)),
                                                                 _title=obj.title)

        # 更新数据库中的用户余额
        UserDetails.objects.filter(user_id=uid).update(balance=F('balance') + change_balance)

        # 获取此用户更新后的balance
        user_obj = UserDetails.objects.filter(user_id=uid).first()

        # 创建余额变动清单
        BalanceInfo.objects.create(
            user_id=uid,
            balance_type=balance_type,
            balance=change_balance,
            marks=marks,
            last_balance=user_obj.balance
        )

        # 收到感谢，要查找是谁收到感谢，然后更新此用户的session数据
        session = SessionStore(session_key=obj.author.session)
        # 如果用户在线，才更新
        if session.get('user_info', None):
            session['user_info']['balance'] = user_obj.balance
            # 在外边使用session 要调用save 保存数据
            session.save()

    # 主题收到回复
    elif update_type == 'reply_recv':
        uid = obj.author_id
        change_balance = 5
        balance_type = "主题回复收益"
        marks = '主题 > <a href="{_uri}">{_title}</a> 收到了回复'.format(_uri=reverse('topic', args=(obj.topic_sn,)),
                                                                  _title=obj.title)

        # 更新数据库中的用户余额
        UserDetails.objects.filter(user_id=uid).update(balance=F('balance') + change_balance)

        # 获取此用户更新后的balance
        user_obj = UserDetails.objects.filter(user_id=uid).first()

        # 创建余额变动清单
        BalanceInfo.objects.create(
            user_id=uid,
            balance_type=balance_type,
            balance=change_balance,
            marks=marks,
            last_balance=user_obj.balance
        )

        # 收到回复，要查找是谁收到回复，然后更新此用户的session数据
        session = SessionStore(session_key=obj.author.session)
        if session.get('user_info', None):
            session['user_info']['balance'] = user_obj.balance
            # 在外边使用session 要调用save 保存数据
            session.save()

    # 编辑主题
    elif update_type == 'edit':
        uid = obj.author_id
        change_balance = -5
        balance_type = "编辑主题"
        marks = '编辑了主题 > <a href="{_uri}">{_title}</a>'.format(_uri=reverse('topic', args=(obj.topic_sn,)),
                                                               _title=obj.title)

        # 更新数据库中的用户余额
        UserDetails.objects.filter(user_id=uid).update(balance=F('balance') + change_balance)

        # 获取此用户更新后的balance
        user_obj = UserDetails.objects.filter(user_id=uid).first()

        # 创建余额变动清单
        BalanceInfo.objects.create(
            user_id=uid,
            balance_type=balance_type,
            balance=change_balance,
            marks=marks,
            last_balance=user_obj.balance
        )
        # 更新session 中数据
        request.session['user_info']['balance'] = user_obj.balance
