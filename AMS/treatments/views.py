from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404,redirect,HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin
from django.views.generic import ListView,FormView,CreateView,UpdateView
from treatments.forms import FeedbackForm,TreatmentForm,PrescriptionForm
from treatments.models import Treatment,Prescription,Feedback

# List View For Each patient's and doctor's all Treatments 
class TreatmentView(LoginRequiredMixin,PermissionRequiredMixin,ListView):
    template_name = 'treatments/treatments.html'
    login_url = reverse_lazy('users:login')
    model = Treatment
    permission_required = 'AMS.view_treatment'

    def handle_no_permission(self):
        # Return a custom HTTP response for permission denied
        return HttpResponse("You do not have permission to view this page.", status=403)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
    
        context['user'] = self.request.user
        
        # Determine the role of the user and add role-specific data
        user = self.request.user
        
        if user.groups.filter(name='Patient').exists():
            context['role'] = 'Patient'
            context['Treatments'] = Treatment.objects.filter(patient__user = user).order_by('-date')
           
        elif user.groups.filter(name='Doctor').exists():
            context['role'] = 'Doctor'
            context['Treatments'] = Treatment.objects.filter(doctor__user = user).order_by('-date')
          
        elif user.groups.filter(name='Receptionist').exists():
            context['role'] = 'Receptionist'
            context['Treatments'] = Treatment.objects.all()
           
          
        elif user.groups.filter(name='Admin').exists():
            context['role'] = 'Admin'
            context['Treatments'] = Treatment.objects.all()
        
        return context
    

class TreatmentCreateView(LoginRequiredMixin, PermissionRequiredMixin,CreateView):
    model = Treatment
    login_url = reverse_lazy('users:login')
    form_class = TreatmentForm
    template_name = 'treatments/treatment_form.html'
    success_url = reverse_lazy('treatments:treatment_list')
    permission_required = 'AMS.add_treatment'

    def handle_no_permission(self):
        # Return a custom HTTP response for permission denied
        return HttpResponse("You do not have permission to view this page.", status=403)
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['prescription_form'] = PrescriptionForm(self.request.POST)
        else:
            context['prescription_form'] = PrescriptionForm()
        return context
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        # Pass the logged-in user to the form
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        context = self.get_context_data()
        prescription_form = context['prescription_form']
        if prescription_form.is_valid():
            # Save the treatment form
            self.object = form.save()
            # Save the prescription form with the treatment
            prescription = prescription_form.save(commit=False)
            prescription.treatment = self.object
            prescription.save()
            return redirect(self.success_url)
        else:
            return self.render_to_response(self.get_context_data(form=form))


class TreatmentUpdateView(LoginRequiredMixin, PermissionRequiredMixin,UpdateView):
    model = Treatment
    login_url = reverse_lazy('users:login')
    form_class = TreatmentForm
    template_name = 'treatments/treatment_form.html'
    success_url = reverse_lazy('treatments:treatment_list')
    permission_required = 'AMS.change_treatment'

    def handle_no_permission(self):
        # Return a custom HTTP response for permission denied
        return HttpResponse("You do not have permission to view this page.", status=403)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['prescription_form'] = PrescriptionForm(self.request.POST, instance=self.object.prescriptions)
        else:
            context['prescription_form'] = PrescriptionForm(instance=self.object.prescriptions)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        prescription_form = context['prescription_form']
        if prescription_form.is_valid():
            self.object = form.save()
            # Save or update the prescription form with the treatment
            prescription = prescription_form.save(commit=False)
            prescription.treatment = self.object
            prescription.save()
            return redirect(self.success_url)
        else:
            return self.render_to_response(self.get_context_data(form=form))

    def get_object(self, queryset=None):
        # Override get_object to handle the correct Treatment object
        obj = super().get_object(queryset)
        # Prepopulate the prescription form with the existing prescription
        if not hasattr(obj, 'prescriptions'):
            # Create an empty Prescription if none exists
            Prescription.objects.create(treatment=obj)
        return obj
    

class FeedbackFormView(LoginRequiredMixin,PermissionRequiredMixin,FormView):
    form_class = FeedbackForm
    login_url =reverse_lazy('users:login')
    template_name = 'treatments/feedback.html'
    success_url = reverse_lazy('treatments:treatment_list')
    permission_required = 'AMS.add_feedback'

    def handle_no_permission(self):
        # Return a custom HTTP response for permission denied
        return HttpResponse("You do not have permission to view this page.", status=403)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        treatment_id = self.kwargs['treatment_id']
        context['treatment'] = get_object_or_404(Treatment, id=treatment_id)
        return context

    def form_valid(self, form):
        treatment_id = self.kwargs['treatment_id']
        treatment = get_object_or_404(Treatment, id=treatment_id)

        # setting treatment id and user manually from the logged in user
        form.instance.treatment = treatment
        form.instance.patient = self.request.user.patient_profile 

        form.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        return super().form_invalid(form)
