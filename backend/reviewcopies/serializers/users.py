from rest_framework import serializers

from reviewcopies import models

__all__ = ["UserDetailSerializer"]


class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ["uuid","username","pk", "last_name", "first_name", "role"]
