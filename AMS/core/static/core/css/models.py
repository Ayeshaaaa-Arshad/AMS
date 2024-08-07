from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractUser
from .validators import validate_image_file_extension
from .CustomManager import AppointmentManager, UserManager

class CustomUser(AbstractUser):
    GENDER_TYPE = [
        ("F", "Female"),
        ("M", "Male"),
        ("O", "Other")
    ]

    gender = models.CharField(max_length=1, choices=GENDER_TYPE)
    image = models.ImageField(upload_to='profile/images', verbose_name='Profile Image', blank=True, null=True, validators=[validate_image_file_extension])
    email = models.EmailField(unique=True)
    username = None

    USERNAME_FIELD = 'email'  # setting Email for log in
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Patient(models.Model):
    user = models.OneToOneField(CustomUser, related_name='patient_profile', on_delete=models.CASCADE)
    age = models.PositiveIntegerField()

    class Meta:
        verbose_name = "Patient"
        verbose_name_plural = "Patients"

    def __str__(self):
        return f"Patient: {self.user.first_name} {self.user.last_name}, Age: {self.age}"


class Doctor(models.Model):
    user = models.OneToOneField(CustomUser, related_name='doctor_profile', on_delete=models.CASCADE)
    designation = models.CharField(max_length=255)

    class Meta:
        verbose_name = "Doctor"
        verbose_name_plural = "Doctors"

    def __str__(self):
        return f"Doctor: {self.user.first_name} {self.user.last_name}, Designation: {self.designation}"


class Receptionist(models.Model):
    user = models.OneToOneField(CustomUser, related_name='receptionist_profile', on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Receptionist"
        verbose_name_plural = "Receptionists"

    def __str__(self):
        return f"Receptionist: {self.user.first_name} {self.user.last_name}"


class Disease(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return f"Disease: {self.name}"


class Appointment(models.Model):
    PENDING = 'Pending'
    COMPLETE = 'Complete'
    CANCELLED = 'Cancelled'
    
    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (COMPLETE, 'Complete'),
        (CANCELLED, 'Cancelled')
    ]

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


class Treatment(models.Model):
    patient = models.ForeignKey(Patient, related_name='treatment', on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, related_name='treatment', on_delete=models.CASCADE)
    disease = models.ForeignKey(Disease, related_name='treatment', on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now())
    remarks = models.TextField(max_length=255)

    def __str__(self):
        return f"Treatment: - Patient {self.patient} Doctor: {self.doctor} - Remarks: {self.remarks}"


class Prescription(models.Model):
    treatment = models.OneToOneField(Treatment, related_name='prescriptions', on_delete=models.CASCADE)
    details = models.TextField(max_length=255)

    def __str__(self):
        return f"Prescription for Treatment ID {self.treatment.id}: {self.details}"


class Announcement(models.Model):
    creator = models.ForeignKey(CustomUser, related_name='announcements', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(max_length=255)
    is_deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Announcement by {self.creator}: {self.description}"


class Feedback(models.Model):
    treatment = models.OneToOneField(Treatment, on_delete=models.CASCADE, related_name='feedback')
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)]) # choices from 1 to 5 to rate the treatment
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback for Appointment ID {self.treatment.id}: Rating {self.rating}"
