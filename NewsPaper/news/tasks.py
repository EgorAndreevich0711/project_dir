from datetime import datetime, timedelta
from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from django.utils import timezone
from news.models import Post, Category, Subscription
import logging

logger = logging.getLogger(__name__)

# Ваш существующий код сигнала в виде Celery-задачи
@shared_task
def send_notifications_task(user_email, username, post_id, category_name):
    """Адаптация вашего сигнала для Celery"""
    try:
        post = Post.objects.get(id=post_id)
        html_content = render_to_string(
            'news/newsletter_email.html',
            {
                'user': {'username': username, 'email': user_email},
                'post': post,
                'category_name': category_name,
                'site_url': settings.SITE_URL
            }
        )

        msg = EmailMultiAlternatives(
            subject=f"Новая статья в категории '{category_name}'",
            body=html_content,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[user_email]
        )
        msg.attach_alternative(html_content, 'text/html')
        msg.send()
        logger.info(f"Уведомление отправлено {user_email}")
    except Exception as e:
        logger.error(f"Ошибка отправки: {e}")

@shared_task
def send_weekly_digest():

    last_week = timezone.now() - timedelta(days=7)
    new_posts = Post.objects.filter(created_at__gte=last_wеek, post_type='news')

    if not new_posts.exists():
        return

    subscribers = Subscription.objects.filter(is_active=True).select_related('user')

    for sub in subscribers:
        user_categories = sub.subscriptions.all()
        posts = new_posts.filter(postCategory__in=user_categories).distinct()

        if posts.exists():
            context = {
                'posts': posts,
                'username': sub.user.username,
                'site_url': settings.SITE_URL
            }

            html_content = render_to_string('news/weekly_email.html', context)

            msg = EmailMultiAlternatives(
                subject="Еженедельная подборка новостей",
                body="Новые статьи за неделю",
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[sub.user.email]
            )
            msg.attach_alternative(html_content, "text/html")
            msg.send()