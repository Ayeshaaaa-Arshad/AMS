from django.core.management.base import BaseCommand
from django_celery_beat.models import PeriodicTask, IntervalSchedule


class Command(BaseCommand):
    help = 'Create a periodic task'

    def handle(self, *args, **kwargs):
        # Creating an interval schedule
        schedule, created = IntervalSchedule.objects.get_or_create(
            every=10,
            period=IntervalSchedule.SECONDS
        )

        # Creating the periodic task
        PeriodicTask.objects.get_or_create(
            interval=schedule,
            name='Execute my task every 10 seconds',
            task='core.tasks.my_task'
        )

        self.stdout.write(self.style.SUCCESS('Periodic task created successfully'))
