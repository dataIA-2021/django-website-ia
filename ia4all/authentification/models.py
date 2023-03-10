from django.db import models
from django.contrib.auth.models import AbstractUser

class Utilisateur(AbstractUser):
    photo = models.ImageField()

class CsvFile(models.Model):
    file_name = models.CharField(max_length=255)
    file_path = models.CharField(max_length=255)
    uploaded_at = models.DateTimeField(auto_now_add=True)
