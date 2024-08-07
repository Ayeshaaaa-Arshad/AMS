from .forms import *
from .models import *
from .constants import *
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.shortcuts import render,get_object_or_404,redirect,HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin
from django.views.generic import ListView,FormView,View


# List View For Each patient's and doctor's all Appointments 
class AppointmentView(LoginRequiredMixin,PermissionRequiredMixin,ListView):
    model = Appointment
    login_url = reverse_lazy('users:login')
    template_name = 'appointments/appointments.html'
    permission_required = 'AMS.view_appointment'

    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            # Redirect to login page if the user is not authenticated
            return redirect(self.get_login_url())
        else:
            # Return a custom HTTP response for permission denied
            return HttpResponse("You do not have permission to view this page.", status=403)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['user'] = self.request.user
        
        # Determine the role of the user and add role-specific data
        user = self.request.user
        
        if user.groups.filter(name='Patient').exists():
            context['role'] = 'Patient'
            context['Appointments'] = Appointment.objects.filter(patient__user = user).order_by('-appointment_date')
           
        elif user.groups.filter(name='Doctor').exists():
            context['role'] = 'Doctor'
            context['Appointments'] = Appointment.objects.filter(doctor__user = user).order_by('-appointment_date')
          
        elif user.groups.filter(name='Receptionist').exists():
            context['role'] = 'Receptionist'
            context['Appointments'] = Appointment.objects.all()
           
        elif user.groups.filter(name='Admin').exists():
            context['role'] = 'Admin'
            context['Appointments'] = Appointment.objects.all()
        
        return context


class BookAppointmentView(LoginRequiredMixin,PermissionRequiredMixin, FormView):
    template_name = 'appointments/book_appointment.html'
    login_url = reverse_lazy('users:login')
    form_class = AppointmentForm
    permission_required = 'AMS.add_appointment'

    # Override handle_no_permission to customize the behavior when permission is denied
    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            # Redirect to login page if the user is not authenticated
            return redirect(self.get_login_url())
        else:
            # Return a custom HTTP response for permission denied
            return HttpResponse("You do not have permission to view this page.", status=403)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['diseases'] = Disease.objects.all()
        user = self.request.user

        # Determine the role of the user and add role-specific data
        if user.groups.filter(name='Admin').exists() or user.groups.filter(name='Receptionist').exists():
            context['patients'] = Patient.objects.all()
            context['role'] = 'Admin' if user.groups.filter(name='Admin').exists() else 'Receptionist'
        elif user.groups.filter(name='Patient').exists():
            if hasattr(user, 'patient_profile'):
                context['patients'] = [user.patient_profile]
            context['role'] = 'Patient'

        context['doctors'] = Doctor.objects.all()
        return context

    def form_valid(self, form):
        user = self.request.user

        # Determine the role of the user and assign the patient
        if user.groups.filter(name='Patient').exists():
            if hasattr(user, 'patient_profile'):
                form.instance.patient = user.patient_profile
            else:
                form.add_error(None, "Patient profile not found.")
                return self.form_invalid(form)

        if user.groups.filter(name='Admin').exists() or user.groups.filter(name='Receptionist').exists():
            patient_id = self.request.POST.get('patient')
            if patient_id:
                try:
                    form.instance.patient = Patient.objects.get(id=patient_id)
                except Patient.DoesNotExist:
                    form.add_error(None, "Selected patient does not exist.")
                    return self.form_invalid(form)
            else:
                form.add_error(None, "Patient must be selected.")
                return self.form_invalid(form)

        form.instance.status = PENDING
        form.instance.doctor = form.cleaned_data['doctor']
        form.save()
        return redirect(reverse_lazy('appointments:appointment_list'))

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))

    
class UpdateAppointmentView(LoginRequiredMixin,PermissionRequiredMixin, View):
    login_url = reverse_lazy('users:login')
    permission_required = 'AMS.change_appointment'

     # Override handle_no_permission to customize the behavior when permission is denied
    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            # Redirect to login page if the user is not authenticated
            return redirect(self.get_login_url())
        else:
            # Return a custom HTTP response for permission denied
            return HttpResponse("You do not have permission to view this page.", status=403)
        
    def get(self, request, pk):
        appointment = get_object_or_404(Appointment, pk=pk)
        if not (request.user.groups.filter(name='Receptionist').exists() or request.user.groups.filter(name='Admin').exists()):
            return redirect('forbidden')  # Redirect to forbidden page if unauthorized

        form = AppointmentForm(instance=appointment)
        return render(request, 'appointments/update_appointment.html', {'form': form, 'appointment': appointment})

    def post(self, request, pk):
        appointment = get_object_or_404(Appointment, pk=pk)
        if not (request.user.groups.filter(name='Receptionist').exists() or request.user.groups.filter(name='Admin').exists()):
            return redirect('users:login')  # Redirect to login page if unauthorized

        form = AppointmentForm(request.POST, instance=appointment)
        if form.is_valid():
            form.save()
            return redirect('appointments:appointment_list')
        return render(request, 'appointments/update_appointment.html', {'form': form, 'appointment': appointment})


class CancelAppointmentView(LoginRequiredMixin,PermissionRequiredMixin, View):
    login_url = reverse_lazy('users:login')
    permission_required = 'AMS.delete_appointment'

     # Override handle_no_permission to customize the behavior when permission is denied
    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            # Redirect to login page if the user is not authenticated
            return redirect(self.get_login_url())
        else:
            # Return a custom HTTP response for permission denied
            return HttpResponse("You do not have permission to view this page.", status=403)
        
    def post(self, request, pk):
        appointment = get_object_or_404(Appointment, pk=pk)
        if (request.user.groups.filter(name='Doctor').exists()):
            return redirect('login')  # Redirect to login page if unauthorized

        appointment.status = CANCELLED 
        appointment.save()
        return redirect('appointments:appointment_list')
    