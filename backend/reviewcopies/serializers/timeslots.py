from rest_framework import serializers
from reviewcopies.models import Timeslot
from reviewcopies.serializers import schedules

class TimeslotSerializer(serializers.ModelSerializer):
    schedule = schedules.ScheduleListSerializer(read_only=True)
    class Meta:
        model = Timeslot
        fields = ['pk', 'uuid', 'begin_time', 'end_time', 'schedule']
