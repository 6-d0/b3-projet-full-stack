from django.utils import timezone
from rest_framework import serializers

from reviewcopies.models import Course, Registration, Timeslot, User
from reviewcopies.serializers.courses import CourseListSerializer
from reviewcopies.serializers.timeslots import TimeslotSerializer
from reviewcopies.serializers.users import UserDetailSerializer


class RegistrationSerializer(serializers.ModelSerializer):
    course = CourseListSerializer(read_only=True)
    slot = TimeslotSerializer(read_only=True)
    student = UserDetailSerializer(read_only=True)

    class Meta:
        model = Registration
        fields = ["id", "uuid", "date", "comment", "course", "student", "slot"]


class AddRegistrationSerializer(serializers.ModelSerializer):
    course = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all())
    slot = serializers.PrimaryKeyRelatedField(queryset=Timeslot.objects.all())
    student = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Registration
        fields = [
            "course",
            "slot",
            "student",
            "comment",
        ]

    def validate(self, attrs):
        student = attrs.get("student")
        course = attrs.get("course")
        slot = attrs.get("slot")

        if isinstance(slot, int):
            slot = Timeslot.objects.get(id=slot)
        if isinstance(course, int):
            course = Course.objects.get(id=course)
        student_slots = Registration.objects.filter(student=student)
        for student_slot in student_slots:
            if student_slot.slot.schedule.date == slot.schedule.date:
                student_begin_time_truncated = student_slot.slot.begin_time.replace(
                    year=1, month=1, day=1, second=0, microsecond=0
                ).astimezone(timezone.get_current_timezone())
                slot_begin_time_truncated = slot.begin_time.replace(
                    year=1, month=1, day=1, second=0, microsecond=0
                ).astimezone(timezone.get_current_timezone())

                student_end_time_truncated = student_slot.slot.end_time.replace(
                    year=1, month=1, day=1, second=0, microsecond=0
                ).astimezone(timezone.get_current_timezone())
                slot_end_time_truncated = slot.end_time.replace(
                    year=1, month=1, day=1, second=0, microsecond=0
                ).astimezone(timezone.get_current_timezone())

                # c'est quand je fais ca que je dois retourner en méthode 1ere
                if (
                    (
                        student_begin_time_truncated < slot_end_time_truncated
                        and student_end_time_truncated > slot_begin_time_truncated
                    )
                    or (
                        student_begin_time_truncated < slot_begin_time_truncated
                        and student_end_time_truncated > student_end_time_truncated
                    )
                    or student_begin_time_truncated == slot_begin_time_truncated
                    or student_end_time_truncated == slot_end_time_truncated
                ):
                    raise serializers.ValidationError(
                        f"Vous êtes deja inscrit au cours de {student_slot.course.name} durant ces heures"
                    )

        if slot.schedule.session not in course.sessions.all():
            raise serializers.ValidationError(
                "Le créneau horaire ne correspond pas à la session du cours."
            )
        if len(Registration.objects.filter(slot=slot)) > 0:
            raise serializers.ValidationError("Ce timeslot n'est plus disponible.")
        if Registration.objects.filter(
            course=course, student=student, slot=slot
        ).exists():
            raise serializers.ValidationError(
                "Vous êtes déjà inscrit à ce créneau pour ce cours."
            )
        if Registration.objects.filter(course=course, student=student):
            raise serializers.ValidationError(
                "Vous êtes déjà inscrit à un créneau pour ce cours"
            )
        else:
            print(f"{slot.begin_time} !!")

        return attrs

    def create(self, validated_data):
        request = self.context.get("request")
        validated_data["student"] = request.user
        return super().create(validated_data)
