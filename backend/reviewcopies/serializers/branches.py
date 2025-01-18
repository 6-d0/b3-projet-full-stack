from rest_framework import serializers
from reviewcopies import models
from reviewcopies.models.core import Course
from reviewcopies.serializers.courses import CourseListSerializer
__all__ = ["BranchListSerializer"]


class BranchListSerializer(serializers.ModelSerializer):
    courses = CourseListSerializer(many=True)
    class Meta:
        model = models.Branch
        fields = ["slug", "uuid", "name" , "pk", "courses"]
