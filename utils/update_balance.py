from operation.models import BalanceInfo, UserDetails


def update_balance(request, update_type, obj=None):

    # 创建主题
    if update_type == 'create':
        # 获取当前余额
        current_balance = request.session.get('user_info')['balance']
        # 获取当前用户的id
        uid = request.session.get('user_info')['uid']
        # 设置改变值
        change_balance = -20
        # 类型
        balance_type = "创建主题"
        # 描述
        marks = '创建了的主题 {_title}'.format(_title=obj.title)

    # 创建回复
    elif update_type == 'reply':
        current_balance = request.session.get('user_info')['balance']
        uid = request.session.get('user_info')['uid']
        change_balance = -5
        balance_type = "创建回复"
        marks = '在主题 {_title} 中创建了回复'.format(_title=obj.title)

    # 感谢主题
    elif update_type == 'thanks':
        current_balance = request.session.get('user_info')['balance']
        uid = request.session.get('user_info')['uid']
        change_balance = -15
        balance_type = "发送谢意"
        marks = '感谢 {_author} 的主题 > {_title}'.format(_author=obj.author.username, _title=obj.title)

    # 收到感谢
    elif update_type == 'recv_thanks':
        user_obj = UserDetails.objects.filter(user_id=obj.author_id).first()
        current_balance = user_obj.balance
        uid = obj.author_id
        change_balance = 10
        balance_type = "收到谢意"
        marks = '主题 {_title} 收到感谢'.format(_title=obj.title)

    # 主题收到回复
    elif update_type == 'reply_recv':
        user_obj = UserDetails.objects.filter(user_id=obj.author_id).first()
        current_balance = user_obj.balance
        uid = obj.author_id
        change_balance = 5
        balance_type = "主题回复收益"
        marks = '主题 {_title} 收到了回复'.format(_title=obj.title)

    # 编辑主题
    elif update_type == 'edit':
        user_obj = UserDetails.objects.filter(user_id=obj.author_id).first()
        current_balance = user_obj.balance
        uid = obj.author_id
        change_balance = -5
        balance_type = "编辑主题"
        marks = '编辑主题 {_title}'.format(_title=obj)

    # 创建余额变动清单
    BalanceInfo.objects.create(
        user_id=uid,
        balance_type=balance_type,
        balance=change_balance,
        marks=marks,
        last_balance=current_balance + change_balance
    )

    # 更新数据库中的用户余额
    user_obj = UserDetails.objects.filter(user_id=uid).first()
    user_obj.balance = current_balance + change_balance
    user_obj.save()

    # 更新session信息 已经在中间件中做了
    # request.session['user_info']['balance'] = current_balance + change_balance
