import logging
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from django.template.loader import render_to_string

from news.models import PostCategory, Post

logger = logging.getLogger(__name__)

def send_notifications(user,post, category_name):
    try:
        html_content = render_to_string(
            'news/newsletter_email.html',
            {'user': user,
                    'post': post,
                    'category_name': category_name,


             }
        )
    except Exception as e:
        logger.error(f"Ошибка рендеринга шаблона для пользователя {user.username}: {e}")
        html_content = f"Ошибка при формировании HTML письма.  Обратитесь к администратору.\n\n{e}"

    subject = f"Новая статья в категории '{category_name}'"

    msg = EmailMultiAlternatives(
        subject=subject,
        body=html_content,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[user.email]
    )

    msg.attach_alternative(html_content, 'text/html')
    try:
        msg.send()
        logger.info(f"Уведомление отправлено пользователю {user.username} о посте {post.title} в категории {category_name}")
    except Exception as e:
        logger.error(f"Ошибка отправки письма пользователю {user.username}: {e}")


@receiver(m2m_changed, sender=PostCategory)
def notify_about_new_post(sender, instance, **kwargs):
    logger.info(f"Сигнал m2m_changed получен для поста {instance.title}, действие: {kwargs['action']}")
    if kwargs['action'] == 'post_add':
        categories = instance.postCategory.all()
        for category in categories:
            for subscriber in category.subscribers.all():
                logger.info(f"Отправка уведомления пользователю {subscriber.username} о посте {instance.title} в категории {category.name}")
                send_notifications(subscriber, instance, category.name)
    elif kwargs['action'] == 'post_remove':
        logger.info(f"Категория удалена из поста {instance.title}.  Действие не определено.")
