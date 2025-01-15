import uuid

from django.db import models

__all__ = ["BaseModel"]


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True
