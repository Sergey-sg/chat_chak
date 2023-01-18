from celery import shared_task
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from apps.account.tokens import account_activation_token
from django.utils.translation import gettext_lazy as _


def send_activate_message(user, request) -> None:
    """send message for new user with activate link"""
    to_email = user.email
    current_site = get_current_site(request)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = account_activation_token.make_token(user)
    message = render_to_string(
        'registration/msg.jinja2',
        {
            'domain': current_site.domain,
            'uid': uid,
            'token': token,
        }
    )
    task_send_mail.delay(to_email=to_email, message=message)


@shared_task(bind=True, default_retry_delay=5*60)
def task_send_mail(self, to_email, message):
    try:
        send_mail(
            _('Activating your account'),
            from_email=settings.EMAIL_HOST_USER,
            message=_('link to confirm email and complete registration'),
            recipient_list=[to_email],
            html_message=message,
        )
        print(f'sending activation token to "{to_email}" completed')
    except Exception as exc:
        raise self.retry(exc=exc, countdown=60)
