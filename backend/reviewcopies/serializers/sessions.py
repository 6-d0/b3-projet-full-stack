from rest_framework import serializers
from reviewcopies import models

__all__ = ["SessionListSerializer"]


class SessionListSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Session
        fields = ["pk", "uuid", "slug", "name"]
