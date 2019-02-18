from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template


def send_message(subject, to, template, context, **kwargs):
    tpl_ns = '/'.join(['emails', template])
    text = get_template('/'.join([tpl_ns, 'template.txt']))
    html = get_template('/'.join([tpl_ns, 'template.html']))

    text_content = text.render(context)
    html_content = html.render(context)

    from_email = kwargs.get('from_email', settings.DEFAULT_FROM_EMAIL)
    reply_to = kwargs.get('reply_to', None)

    msg = EmailMultiAlternatives(
        subject=subject,
        body=text_content,
        from_email=from_email,
        to=[to],
        reply_to=reply_to,
    )
    msg.attach_alternative(html_content, 'text/html')
    msg.send()
