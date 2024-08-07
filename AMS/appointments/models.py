from core.models import *
from users.models import *
from django.db import models
from .constants import STATUS_CHOICES,PENDING
from .CustomManager import AppointmentManager
from .exceptions import AppointmentDateException
from django.core.exceptions import ValidationError



class Appointment(models.Model):
    
    class Meta :
        db_table = 'ams_appointment'

    patient = models.ForeignKey(Patient, related_name='appointments', on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, related_name='appointments', on_delete=models.CASCADE)
    disease = models.ForeignKey(Disease, related_name='appointments', on_delete=models.CASCADE)
    appointment_date = models.DateTimeField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=PENDING)

    objects = AppointmentManager()  # Custom Manager for Appointments

    def __str__(self):
        return f"Appointment: {self.patient} with {self.doctor} on {self.appointment_date}"

    def clean(self):
        # Call the parent class's clean method
        super().clean()

        # Check if the patient and doctor are the same user
        if self.patient and self.doctor:
            if self.patient.user == self.doctor.user:
                raise ValidationError('A patient cannot be the same as the doctor and vice versa.')
            
        # Check if the appointment date is in the past
        # if self.appointment_date < timezone.now():
        #     raise AppointmentDateException()
