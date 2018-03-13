from django.core.mail import send_mail
from django.urls import reverse
from v2ex.settings import EMAIL_FROM, BASE_DOMAIN


EMAIL_TMPLATE = '''
亲爱的假的V2EX社区用户： 

您的验证码是: {_code}
<span style="color:#4F81BD;">34HRAWLyTHw</span>

此信是由假的V2EX社区系统发出，系统不接受回信，请勿直接回复。 
如有任何疑问，请联系我们。 

致 
礼！ 

假的V2EX社区——假的，假的，假的
<a href="http://fv2ex.izhihu.me">http://fv2ex.izhihu.me</a>
'''

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


def send_email_code(to, code):
    msg = ACTIVE_EMAIL.format(_url=BASE_DOMAIN + reverse('activate_email', args=(code,)))
    try:
        send_mail('[FV2EX] 欢迎来到 假的V2EX',
                  '',
                  EMAIL_FROM,
                  [to],
                  html_message=msg)
        return True
    except Exception as e:
        print(e)
        return False
