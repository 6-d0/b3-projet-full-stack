from rest_framework import serializers
from reviewcopies import models
from reviewcopies.serializers import users
class CourseListSerializer(serializers.ModelSerializer):
    teacher_name = serializers.CharField(source="teacher.get_full_name", read_only=True)
    session_name = serializers.CharField(source="session.name", read_only=True)
    teacher = users.UserDetailSerializer(read_only=True)
    class Meta:
        model = models.Course
        fields = ["id", "name", "slug", "teacher_name", "teacher", "session_name"]
