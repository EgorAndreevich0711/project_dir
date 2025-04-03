import logging
from django.conf import settings
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore
from django_apscheduler.models import DjangoJobExecution
from django.utils import timezone
from django.contrib.auth.models import User
from news.models import Category, Post
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
import datetime

logger = logging.getLogger(__name__)


def send_weekly_newsletter():
    today = timezone.now()
    last_week = today - datetime.timedelta(weeks=1)

    for category in Category.objects.all():
        subscribers = category.subscribers.all()
        if subscribers.exists():
            new_posts = Post.objects.filter(
                postCategory=category,
                dateCreation__range=(last_week, today)
            )

            if new_posts.exists():
                for subscriber in subscribers:
                    html_content = render_to_string(
                        'news/weekly_email.html',
                        {
                            'user': subscriber,
                            'category': category,
                            'posts': new_posts,
                            'site_url': settings.SITE_URL,
                        }
                    )

                    subject = f"Еженедельная рассылка: Новые статьи в категории '{category.name}'"
                    msg = EmailMultiAlternatives(
                        subject=subject,
                        body=html_content,
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        to=[subscriber.email]
                    )
                    msg.attach_alternative(html_content, "text/html")
                    try:
                        msg.send()
                        logger.info(f"Отправлена еженедельная рассылка пользователю {subscriber.username} о {new_posts.count()} новых статьях в категории {category.name}.")
                    except Exception as e:
                        logger.error(f"Ошибка отправки еженедельной рассылки пользователю {subscriber.username}: {e}")
            else:
                logger.info(f"Нет новых статей в категории '{category.name}' за последнюю неделю, рассылка не отправлена.")
        else:
            logger.info(f"В категории '{category.name}' нет подписчиков.")


def delete_old_job_executions(max_age=604_800):
    DjangoJobExecution.objects.delete_old_job_executions(max_age)


class Command(BaseCommand):
    help = "Runs apscheduler."

    def handle(self, *args, **options):
        scheduler = BlockingScheduler(timezone=settings.TIME_ZONE)
        scheduler.add_jobstore(DjangoJobStore(), "default")


        scheduler.add_job(
            send_weekly_newsletter,
            trigger=CronTrigger(day_of_week="mon", hour="08", minute="00"),
            id="send_weekly_newsletter",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Added weekly job: 'send_weekly_newsletter'.")

        scheduler.add_job(
            delete_old_job_executions,
            trigger=CronTrigger(
                day_of_week="mon", hour="00", minute="00"
            ),
            id="delete_old_job_executions",
            max_instances=1,
            replace_existing=True,
        )
        logger.info("Scheduler shut down successfully!")