from django import forms
from users.models import *
from appointments.models import *
from .models import Feedback,Treatment,Prescription


#Feedback Form
class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Rate from 1 to 5'}),
            'comment': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Write your feedback'}),
        }


class TreatmentForm(forms.ModelForm):
    class Meta:
        model = Treatment
        fields = ['patient','disease', 'doctor', 'remarks']
        widgets = {
            'remarks': forms.Textarea(attrs={'class': 'form-control'}),
           'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if user:
            if user.groups.filter(name='Admin').exists():
                # Admin can see all patients and doctors
                self.fields['patient'].queryset = Patient.objects.all()
                self.fields['doctor'].queryset = Doctor.objects.all()
            elif user.groups.filter(name='Doctor').exists():
                # Logged-in doctor can see only their own patients
                doctor = user.doctor_profile
                self.fields['patient'].queryset = Patient.objects.filter(
                    id__in=Appointment.objects.filter(doctor=doctor).values_list('patient_id', flat=True)
                )
                self.fields['doctor'].queryset = Doctor.objects.filter(id=doctor.id)
            else:
                # Non-admin and non-doctor users see no patients and doctors
                self.fields['patient'].queryset = Patient.objects.none()
                self.fields['doctor'].queryset = Doctor.objects.none()

        # Debug output
        print(f"User: {user}")
        print(f"Patient queryset: {self.fields['patient'].queryset.query}")
        print(f"Doctor queryset: {self.fields['doctor'].queryset.query}")


#PrescriptionForm
class PrescriptionForm(forms.ModelForm):
    class Meta:
        model = Prescription
        fields = ['details']
