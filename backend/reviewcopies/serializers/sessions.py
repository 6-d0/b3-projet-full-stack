from rest_framework import serializers
from reviewcopies import models
__all__ = ["SessionListSerializer"]


class SessionListSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Session
        fields = ["pk", "uuid", "slug", "name"]

def get_default_courses():
    return models.Course.objects.all()
class CreateSessionSerializer(serializers.ModelSerializer):

    courses = serializers.PrimaryKeyRelatedField(
        queryset=models.Course.objects.all(),
        many=True,
        required=False,
        allow_null=True,
        default=models.Course.objects.all())


    class Meta:
        model = models.Session
        fields = ["pk", "uuid", "name", "courses"]
