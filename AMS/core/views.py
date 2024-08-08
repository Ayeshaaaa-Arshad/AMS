from datetime import datetime, timedelta
from django.urls import reverse_lazy
from django.shortcuts import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin
from django.views.generic import ListView,TemplateView,DetailView,CreateView,DeleteView,UpdateView
from core.forms import AnnouncementForm
from core.models import Disease,Announcement
from treatments.models import Treatment
from users.models import Patient,Doctor,Receptionist

class IndexPageView(LoginRequiredMixin, TemplateView):
    template_name = 'core/index.html'
    login_url = reverse_lazy('users:login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
    
        #Common context data
        context['Announcements'] = Announcement.objects.filter(
            is_deleted=False,
            created_at__gte=datetime.now()-timedelta(days=30)
        )

        # Determine the role of the user and add role-specific data
        user = self.request.user

        context['user'] = user

        
        if user.groups.filter(name='Patient').exists():
            context['role'] = 'Patient'
            context['DataForGrid'] = Doctor.objects.all()[:2]
            context['Treatment'] = Treatment.objects.filter(patient__user=user).last()
           

        elif user.groups.filter(name='Doctor').exists():
            context['role'] = 'Doctor'
            context['DataForGrid'] = Patient.objects.all()[:2]
            context['Treatment'] = Treatment.objects.filter(doctor__user=user).last()
      
          
        elif user.groups.filter(name='Receptionist').exists():
            context['role'] = 'Receptionist'
            context['DataForGrid'] = Doctor.objects.all()[:2]
            
          
        elif user.groups.filter(name='Admin').exists():
            context['role'] = 'Admin'
             # Get counts of Patients, Doctors, and Receptionists
            context['patient_count'] = Patient.objects.count()
            context['doctor_count'] = Doctor.objects.count()
            context['receptionist_count'] = Receptionist.objects.count()

        
        return context

class DiseaseCreateView(LoginRequiredMixin,PermissionRequiredMixin, CreateView):
    model = Disease
    login_url = reverse_lazy('users:login')
    fields = ['name', 'description']
    template_name = 'core/disease_form.html'
    success_url = reverse_lazy('core:disease_list')
    permission_required = 'core.add_disease'

    def handle_no_permission(self):
        # Return a custom HTTP response for permission denied
        return HttpResponse("You do not have permission to view this page.", status=403)

    def form_valid(self, form):
        if self.request.user.groups.first().name != 'Admin':
            return self.handle_no_permission()
        return super().form_valid(form)


class DiseaseUpdateView(LoginRequiredMixin,PermissionRequiredMixin, UpdateView):
    model = Disease
    login_url = reverse_lazy('users:login')
    fields = ['name', 'description']
    template_name = 'core/disease_form.html'
    success_url = reverse_lazy('core:disease_list')
    permission_required = 'core.change_disease'

    def handle_no_permission(self):
        # Return a custom HTTP response for permission denied
        return HttpResponse("You do not have permission to view this page.", status=403)

    def form_valid(self, form):
        #checking the permissions
        if self.request.user.groups.first().name != 'Admin':
            return self.handle_no_permission()
        return super().form_valid(form)


class DiseaseDeleteView(LoginRequiredMixin,PermissionRequiredMixin, DeleteView):
    model = Disease
    login_url = reverse_lazy('users:login')
    template_name = 'core/disease_confirm_delete.html'
    success_url = reverse_lazy('core:disease_list')
    permission_required = 'core.delete_disease'

    def handle_no_permission(self):
        # Return a custom HTTP response for permission denied
        return HttpResponse("You do not have permission to view this page.", status=403)

    def form_valid(self, form):
        if self.request.user.groups.first().name != 'Admin':
            return self.handle_no_permission()
        return super().form_valid(form)
    

class DiseaseListView(LoginRequiredMixin,PermissionRequiredMixin, ListView):
    model = Disease
    login_url = reverse_lazy('users:login')
    template_name = 'core/disease_list.html'
    context_object_name = 'diseases'
    permission_required = 'core.view_disease'

    def handle_no_permission(self):
        # Return a custom HTTP response for permission denied
        return HttpResponse("You do not have permission to view this page.", status=403)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # setting user role according to logged user
        user_role = self.request.user.groups.first().name 
        context['role'] = user_role
        return context
    

class AnnouncementListView(LoginRequiredMixin,PermissionRequiredMixin, ListView):
    model = Announcement
    login_url = reverse_lazy('users:login')
    template_name = 'core/announcements.html'
    permission_required = 'AMS.view_announcement'

    def handle_no_permission(self):
        # Return a custom HTTP response for permission denied
        return HttpResponse("You do not have permission to view this page.", status=403)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user = self.request.user
        context['user'] = user
        context['announcements'] = Announcement.objects.filter(is_deleted=False)

        if user.groups.all().exists():
            print(user.groups.all().first())
            context['role'] = str(user.groups.all().first())

        return context


class AnnouncementDetailView(LoginRequiredMixin,PermissionRequiredMixin, DetailView):
    model = Announcement
    login_url = reverse_lazy('users:login')
    template_name = 'core/announcement_detail.html'
    context_object_name = 'announcement'
    permission_required = 'AMS.view_announcement'

    def handle_no_permission(self):
        # Return a custom HTTP response for permission denied
        return HttpResponse("You do not have permission to view this page.", status=403)

class AnnouncementCreateView(LoginRequiredMixin,PermissionRequiredMixin, CreateView):
    model = Announcement
    login_url = reverse_lazy('users:login')
    form_class = AnnouncementForm
    template_name = 'core/announcement_form.html'
    success_url = reverse_lazy('core:announcement_list')
    permission_required = 'AMS.add_announcement'

    def handle_no_permission(self):
        # Return a custom HTTP response for permission denied
        return HttpResponse("You do not have permission to view this page.", status=403)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        form.instance.creator = self.request.user
        return super().form_valid(form)


class AnnouncementUpdateView(LoginRequiredMixin,PermissionRequiredMixin, UpdateView):
    model = Announcement
    login_url = reverse_lazy('users:login')
    fields = ['title', 'description']
    template_name = 'core/announcement_form.html'
    success_url = reverse_lazy('core:announcement_list')
    permission_required = 'AMS.change_announcement'

    def handle_no_permission(self):
        # Return a custom HTTP response for permission denied
        return HttpResponse("You do not have permission to view this page.", status=403)

class AnnouncementDeleteView(LoginRequiredMixin,PermissionRequiredMixin, DeleteView):
    model = Announcement
    login_url = reverse_lazy('users:login')
    template_name = 'core/announcement_confirm_delete.html'
    success_url = reverse_lazy('core:announcement_list')
    permission_required = 'AMS.delete_announcement'

    def handle_no_permission(self):
        # Return a custom HTTP response for permission denied
        return HttpResponse("You do not have permission to view this page.", status=403)
