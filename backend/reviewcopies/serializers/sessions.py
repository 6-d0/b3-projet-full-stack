from rest_framework import serializers

from reviewcopies import models
from reviewcopies.serializers.courses import CourseListSerializer

__all__ = ["SessionListSerializer"]


class SessionListSerializer(serializers.ModelSerializer):
    courses = CourseListSerializer(many=True)

    class Meta:
        model = models.Session
        fields = ["pk", "uuid", "slug", "name", "courses"]


def get_default_courses():
    return models.Course.objects.all()


class CreateSessionSerializer(serializers.ModelSerializer):

    courses = serializers.PrimaryKeyRelatedField(
        queryset=models.Course.objects.all(),
        many=True,
        required=False,
        allow_null=True,
    )

    class Meta:
        model = models.Session
        fields = ["pk", "uuid", "name", "courses"]
