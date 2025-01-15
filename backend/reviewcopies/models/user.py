from django.contrib.auth.models import AbstractUser
from django.db import models
from reviewcopies.models import BaseModel

__all__ = ["User"]


class User(BaseModel, AbstractUser):
    ROLE_CHOICES = (
        ('student', 'Student'),
        ('teacher', 'Teacher'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, blank=True, null=True)
    class Meta(BaseModel.Meta, AbstractUser.Meta):
        pass
