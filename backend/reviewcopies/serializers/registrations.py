from rest_framework import serializers
from reviewcopies.serializers.courses import CourseListSerializer
from reviewcopies.serializers.timeslots import TimeslotSerializer
from reviewcopies.serializers.users import UserDetailSerializer
from reviewcopies.models import Timeslot, Course

from reviewcopies.models import Registration
class RegistrationSerializer(serializers.ModelSerializer):
    course = CourseListSerializer(read_only=True)
    slot = TimeslotSerializer(read_only=True)
    student = UserDetailSerializer(read_only=True)
    class Meta:
        model = Registration
        fields = ['id', 'date', 'comment', 'course', 'student', 'slot']

class AddRegistrationSerializer(serializers.ModelSerializer):
    course = serializers.PrimaryKeyRelatedField(queryset=Course.objects.all())
    slot = serializers.PrimaryKeyRelatedField(queryset=Timeslot.objects.all())


    class Meta:
        model = Registration
        fields = ['course', 'slot', 'student', 'comment']

    def validate(self, attrs):
        student = attrs.get('student')
        course = attrs.get('course')
        slot = attrs.get('slot')
        if isinstance(slot, int):
            slot = Timeslot.objects.get(id=slot)
        if isinstance(course, int):
            course = Course.objects.get(id=course)
        if slot.schedule.session not in course.sessions.all():
            raise serializers.ValidationError("Le créneau horaire ne correspond pas à la session du cours.")

        if Registration.objects.filter(course=course, student=student):
            raise serializers.ValidationError("Vous êtes déjà inscrit à un créneau pour ce cours")
        if Registration.objects.filter(course=course, student=student, slot=slot).exists():
            raise serializers.ValidationError("Vous êtes déjà inscrit à ce créneau pour ce cours.")

        return attrs
    def create(self, validated_data):
        request = self.context.get('request')
        validated_data['student'] = request.user
        return super().create(validated_data)
