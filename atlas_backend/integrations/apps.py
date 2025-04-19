from django.apps import AppConfig
from django.db.utils import OperationalError, ProgrammingError
from django.utils.timezone import now
import json

class IntegrationsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'integrations'

    def ready(self):
        try:
            from django_celery_beat.models import PeriodicTask, IntervalSchedule

            schedule, _ = IntervalSchedule.objects.get_or_create(
                every=1, period=IntervalSchedule.HOURS
            )

            PeriodicTask.objects.get_or_create(
                interval=schedule,
                name='Sync Google Calendar',
                task='integrations.tasks.sync_google_calendar',
                defaults={'start_time': now(), 'args': json.dumps([])},
            )

            PeriodicTask.objects.get_or_create(
                interval=schedule,
                name='Sync Microsoft Calendar',
                task='integrations.tasks.sync_microsoft_calendar',
                defaults={'start_time': now(), 'args': json.dumps([])},
            )

        except (OperationalError, ProgrammingError):
            # Database is not ready yet (e.g., during migrate or initial setup)
            pass
