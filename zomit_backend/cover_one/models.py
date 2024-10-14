from django.db import models
from django.utils import timezone


# Create your models here.
class two_d_cover(models.Model):
    cover_model = models.CharField(max_length=100)
    cover_template = models.CharField(max_length=255)
    created_at = models.DateField(auto_now_add=True)  # Automatically set the field to now when the object is created

    def __str__(self):
        return f"{self.cover_model} - {self.cover_template} ({self.created_at.date()})"
