from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    keterangan = models.CharField(max_length=255)


# Create your models here.
