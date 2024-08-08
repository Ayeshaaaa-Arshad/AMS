from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from core import views

app_name = 'core'

urlpatterns = [
    path('',views.IndexPageView.as_view(),name='index'),
    path('announcements/', views.AnnouncementListView.as_view(), name='announcement_list'),
    path('announcements/<int:pk>/', views.AnnouncementDetailView.as_view(), name='announcement_list'),
    path('announcements/create/', views.AnnouncementCreateView.as_view(), name='announcement_create'),
    path('announcements/<int:pk>/update/', views.AnnouncementUpdateView.as_view(), name='announcement_update'),
    path('announcements/<int:pk>/delete/', views.AnnouncementDeleteView.as_view(), name='announcement_delete'),
    path('diseases/', views.DiseaseListView.as_view(), name='disease_list'),
    path('diseases/create/', views.DiseaseCreateView.as_view(), name='disease_create'),
    path('diseases/update/<int:pk>/', views.DiseaseUpdateView.as_view(), name='disease_update'),
    path('diseases/delete/<int:pk>/', views.DiseaseDeleteView.as_view(), name='disease_delete'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

