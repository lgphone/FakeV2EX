from celery.task import task
from celery import shared_task
from django.core.mail import send_mail
from django.urls import reverse
from v2ex.settings import EMAIL_FROM, BASE_DOMAIN


ACTIVE_EMAIL = '''
<br>
欢迎注册 假的 V2EX 社区。
<br>
<br>
假的 V2EX 是一个创意工作者社区，注册并登录后，你将可以在这里和大家分享你的最新发现，讨论解决各种技术问题，寻找合作伙伴，展示你的作品，任意的奇思妙想，及更多等待你去发现的惊喜。
<br>
<br>
请点击下面的地址验证你的帐号：
<br>
<br>
<a href="{_url}">{_url}</a>
<br>
<br>
如果你有任何疑问，可以回复这封邮件向我们提问。<br>
<br>
假的 V2EX</div>
'''


# 自定义要执行的task任务
@task
def print_hello():
    import time
    time.sleep(10)
    return 'hello django'


@shared_task
def send_email_code(to, code):
    msg = ACTIVE_EMAIL.format(_url=BASE_DOMAIN + reverse('activate_email', args=(code,)))
    ret = {'发送状态': '', 'to': '', 'code': '', 'msg': ''}
    try:
        send_mail('[FV2EX] 欢迎来到 假的V2EX',
                  '',
                  EMAIL_FROM,
                  [to],
                  html_message=msg)
        ret['发送状态'] = "发送成功"
        ret['to'] = to
        ret['code'] = code
        ret['msg'] = True
    except Exception as e:
        ret['发送状态'] = "失败"
        ret['to'] = to
        ret['code'] = code
        ret['msg'] = e

    return ret
