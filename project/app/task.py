from celery import shared_task
from django.contrib.sites.models import Site
from django.core.mail import EmailMessage
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse_lazy
from .models import *


@shared_task
def send_email(pk):
    user = User.objects.get(pk=pk)
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    activation_url = reverse_lazy('activate', kwargs={'uidb64': uid, 'token': token})
    current_site = Site.objects.get_current().domain
    subject = 'Подтвердите свою почту'
    message = render_to_string('app/account_email.html', {
        'user': user,
        'link': f'http://{current_site}{activation_url}',
    })
    email = EmailMessage(subject, message, to=[user.email])
    email.send()