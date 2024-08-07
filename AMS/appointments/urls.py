from . import views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

app_name = 'appointments'

urlpatterns = [
    path('appointments/',views.AppointmentView.as_view(),name='appointment_list'),
    path('book_appointment',views.BookAppointmentView.as_view(),name='book_appointment'),
    path('update_appointment/<int:pk>/', views.UpdateAppointmentView.as_view(), name='update_appointment'),
    path('cancel_appointment/<int:pk>/', views.CancelAppointmentView.as_view(), name='cancel_appointment'),
  ]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

