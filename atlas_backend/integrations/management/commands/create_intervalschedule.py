from django.core.management.base import BaseCommand
from django_celery_beat.models import IntervalSchedule

class Command(BaseCommand):
    help = 'Create default IntervalSchedule for periodic tasks.'

    def handle(self, *args, **kwargs):
        schedule, created = IntervalSchedule.objects.get_or_create(
            every=10,
            period=IntervalSchedule.SECONDS,
        )

        if created:
            self.stdout.write(self.style.SUCCESS('IntervalSchedule created successfully!'))
        else:
            self.stdout.write(self.style.WARNING('IntervalSchedule already exists.'))
