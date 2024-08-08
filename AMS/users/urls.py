from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from users import views

app_name = 'users'

urlpatterns = [
    path('login/',views.LoginView.as_view(),name='login'),
    path('signup/',views.SignupView.as_view(),name='signup'),
    path('logout/', views.logout_user, name='logout'),
    path('doctors/', views.DoctorListView.as_view(), name='doctor_list'),
    path('receptionists/', views.ReceptionistListView.as_view(), name='receptionist_list'),
    path('patients/', views.PatientListView.as_view(), name='patient_list'),
    path('patient/create/', views.PatientCreateView.as_view(), name='patient_create'),
    path('patient/<int:pk>/update/', views.PatientUpdateView.as_view(), name='patient_update'),
    path('patient/<int:pk>/delete/', views.PatientDeleteView.as_view(), name='patient_delete'),
    path('doctors/create/', views.DoctorCreateView.as_view(), name='doctor_create'),
    path('doctors/<int:pk>/edit/', views.DoctorUpdateView.as_view(), name='doctor_update'),
    path('doctors/<int:pk>/delete/', views.DoctorDeleteView.as_view(), name='doctor_delete'),
    path('receptionist/create/', views.ReceptionistCreateView.as_view(), name='receptionist_create'),
    path('receptionist/<int:pk>/edit/', views.ReceptionistUpdateView.as_view(), name='receptionist_update'),
    path('receptionist/<int:pk>/delete/', views.ReceptionistDeleteView.as_view(), name='receptionist_delete'),
    path('edit_profile <int:pk>/',views.EditProfileView.as_view(),name='edit_profile'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

