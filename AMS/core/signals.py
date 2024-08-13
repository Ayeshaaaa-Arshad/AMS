from django.db.models.signals import pre_save
from django.dispatch import receiver
from core.models import DateTimeMixin
from core.middleware import get_current_user

@receiver(pre_save, sender=DateTimeMixin)
def set_updated_by(sender, instance, **kwargs):
    print("IN BASE MODEL________")
    if hasattr(instance, 'updated_by'):
        instance.updated_by = get_current_user()

