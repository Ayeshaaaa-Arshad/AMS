from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from treatments import views

app_name = 'treatments'

urlpatterns = [
    path('treatments/', views.TreatmentView.as_view(), name='treatment_list'),
    path('treatments/create/', views.TreatmentCreateView.as_view(), name='treatment_create'),
    path('treatments/<int:pk>/update/', views.TreatmentUpdateView.as_view(), name='treatment_update'),
    path('treatment/create/', views.TreatmentCreateView.as_view(), name='treatment_create'),
    path('treatment/<int:pk>/update/', views.TreatmentUpdateView.as_view(), name='treatment_update'),
    path('provide_feedback/<int:treatment_id>/',views.FeedbackFormView.as_view(), name='provide_feedback'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

