from django.db.models.signals import pre_save
from django.dispatch import receiver
from core.models import Announcement,Disease
from appointments.models import Appointment
from core.middleware import get_current_user
from treatments.models import Treatment,Feedback,Prescription

@receiver(pre_save, sender=Appointment)
@receiver(pre_save, sender=Treatment)
@receiver(pre_save, sender=Feedback)
@receiver(pre_save, sender=Prescription)
@receiver(pre_save, sender=Disease)
@receiver(pre_save, sender=Announcement)
def set_updated_by(sender, instance, **kwargs):
    if hasattr(instance, 'updated_by'):
        instance.updated_by = get_current_user()
