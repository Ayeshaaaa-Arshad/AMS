from .models import models
from django.db.models import Count
from django.db.models.functions import Coalesce

# Custom Manager Now Appointment will have by default manager's dunctionalities plus these below
class AppointmentManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().order_by('-appointment_date')

    #All patient with their respected count
    def patients_appointments_counts(self):
        return self.get_queryset().filter(status=True).values('patient').annotate(
            count=Coalesce(Count('id'), 0)
        ).order_by('-count')

    #All Doctors with their respected count
    def doctors_appointments_counts(self):
        return self.get_queryset().filter(status=True).values('doctor').annotate(
            count=Coalesce(Count('id'), 0)
        ).order_by('-count')
    