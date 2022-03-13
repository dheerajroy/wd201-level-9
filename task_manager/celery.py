import os
from datetime import datetime, timedelta
from django.conf import settings
from django.core.mail import send_mail
from tasks.models import Task, STATUS_CHOICES
from accounts.models import CustomUser
from celery import Celery
from celery.decorators import periodic_task

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "task_manager.settings")
app = Celery("task_manager")
app.config_from_object("django.conf:settings")
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


# Periodic Task
@periodic_task(run_every=timedelta(seconds=30))
def every_30_seconds():
    print("Running Every 30 Seconds!")
