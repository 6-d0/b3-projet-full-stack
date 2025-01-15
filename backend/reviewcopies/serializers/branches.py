from rest_framework import serializers
from reviewcopies import models

__all__ = ["BranchListSerializer"]


class BranchListSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Branch
        fields = ["slug", "uuid", "name" , "pk"]
