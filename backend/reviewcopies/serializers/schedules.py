from rest_framework import serializers

from reviewcopies import models
from reviewcopies.serializers.sessions import SessionListSerializer


class TeacherDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = ["uuid", "last_name", "first_name", "email", "username"]


class ScheduleListSerializer(serializers.ModelSerializer):
    session = serializers.SlugRelatedField(slug_field="slug", read_only=True)
    teacher = TeacherDetailSerializer()
    session = SessionListSerializer()

    class Meta:
        model = models.Schedule
        fields = [
            "uuid",
            "pk",
            "date",
            "can_subscribe",
            "can_subscribe_until",
            "classroom",
            "teacher",
            "session",
        ]


class ScheduleCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Schedule
        fields = [
            "date",
            "can_subscribe_until",
            "can_subscribe",
            "classroom",
            "session",
        ]

    def validate(self, data):
        if data.get("can_subscribe_until") is not None:
            if data["date"] < data["can_subscribe_until"].date():
                raise serializers.ValidationError(
                    "The subscription date cannot exceed the schedule date."
                )
        if data["classroom"] is not None:
            if models.Schedule.objects.filter(
                classroom=data["classroom"],
                date=data["date"],
                teacher=self.context["request"].user,
            ).exists():
                raise serializers.ValidationError(
                    "This classroom is already scheduled at this date."
                )
        return data

    def create(self, validated_data):
        teacher = self.context["request"].user
        validated_data["teacher"] = teacher
        return super().create(validated_data)
