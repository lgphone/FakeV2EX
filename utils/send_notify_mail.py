from django.core.mail import send_mail
from v2ex.settings import EMAIL_FROM


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


def send_email_code(to, code):
    msg = EMAIL_TMPLATE.format(_code=code)
    send_mail('邮箱验证码',
              '',
              EMAIL_FROM,
              [to],
              html_message=msg)
