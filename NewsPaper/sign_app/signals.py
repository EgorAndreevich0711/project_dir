# sign_app/signals.py
from django.dispatch import receiver
from allauth.account.signals import user_signed_up
from django.core.mail import send_mail
from django.conf import settings

@receiver(user_signed_up)
def send_welcome_email(sender, request, user, **kwargs):
    subject = 'Добро пожаловать на наш новостной портал!'
    message = f'Привет, {user.email}!\n\nСпасибо за регистрацию на нашем сайте! Теперь вы сможете читать свежие новости и подписываться на интересующие вас категории.'
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [user.email]

    send_mail(subject, message, from_email, recipient_list, fail_silently=False)