from django.utils import timezone
from django.db import models
from core.models import Disease, DateTimeMixin
from users.models import Patient, Doctor


class Treatment(DateTimeMixin):
    patient = models.ForeignKey(Patient, related_name='treatment', on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, related_name='treatment', on_delete=models.CASCADE)
    disease = models.ForeignKey(Disease, related_name='treatment', on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)
    remarks = models.TextField(max_length=255)

    class Meta:
        db_table = 'ams_treatment'

    def __str__(self):
        return f"Treatment: - Patient {self.patient} Doctor: {self.doctor} - Remarks: {self.remarks}"


class Prescription(DateTimeMixin):
    treatment = models.OneToOneField(Treatment, related_name='prescriptions', on_delete=models.CASCADE)
    details = models.TextField(max_length=255)

    class Meta:
        db_table = 'ams_prescription'

    def __str__(self):
        return f"Prescription for Treatment ID {self.treatment.id}: {self.details}"


class Feedback(DateTimeMixin):
    treatment = models.OneToOneField(Treatment, on_delete=models.CASCADE, related_name='feedback')
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])  # choices from 1 to 5 to rate the treatment
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'ams_feedback'

    def __str__(self):
        return f"Feedback for Appointment ID {self.treatment.id}: Rating {self.rating}"
