from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = "admin", "Admin"
        OWNER = "owner", "Pet Owner"   

    email = models.EmailField("email address", unique=True)
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.OWNER)
    phone = models.CharField("contact number", max_length=20, blank=True)
    photo = models.ImageField(upload_to="profiles/", blank=True)

    def save(self, *args, **kwargs):
        if self.is_superuser:          
            self.role = self.Role.ADMIN
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username
