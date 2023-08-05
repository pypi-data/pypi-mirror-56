from datetime import datetime, timedelta

from django.core.management.base import BaseCommand
from transcribe import settings
from transcribe.models import UserTask


class Command(BaseCommand):
    help = 'Changes status of old UserTasks to skipped.'

    def handle(self, *args, **options):
        too_old = datetime.now() - timedelta(days=settings.TASK_EXPIRE_DAYS)
        (
            UserTask.objects.filter(
                status='in progress', modified__lt=too_old
            ).update(status='skipped')
        )
