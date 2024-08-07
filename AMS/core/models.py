from users.models import *
from django.db import models
from django.conf import settings
from django.utils import timezone


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )

    class Meta:
        abstract = True

class Disease(BaseModel):
    name = models.CharField(max_length=255)
    description = models.TextField()
    
    class Meta:
        db_table = 'ams_disease'

    def __str__(self):
        return f"Disease: {self.name}"


class Announcement(BaseModel):
    creator = models.ForeignKey(CustomUser, related_name='announcements', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(max_length=255)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        db_table = 'ams_announcement'

    def __str__(self):
        return f"Announcement by {self.creator}: {self.description}"
