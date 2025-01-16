from rest_framework.views import APIView
from django.db.models import Exists, OuterRef
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from reviewcopies.models import Timeslot, Schedule, Registration
from reviewcopies.serializers.timeslots import TimeslotSerializer
from datetime import datetime, timedelta
from django.utils.dateparse import parse_datetime

from reviewcopies.models import Timeslot, Schedule
from reviewcopies.serializers.timeslots import TimeslotSerializer


class TimeslotsByScheduleView(APIView):
    """
    Retrieve all timeslots for a specific schedule.
    Example endpoint:
        GET /api/v1/timeslots/{schedule_id}/
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        schedule_id = kwargs.get("schedule_id")
        schedule = get_object_or_404(Schedule, id=schedule_id)

        timeslots = Timeslot.objects.filter(schedule=schedule).order_by("begin_time")
        serializer = TimeslotSerializer(timeslots, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)



class TimeslotsByScheduleUuidView(APIView):
    """
    Retrieve all timeslots for a specific schedule.
    Example endpoint:
        GET /api/v1/timeslots/{schedule_id}/
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        uuid = kwargs.get("uuid")
        schedule = get_object_or_404(Schedule, uuid=uuid)

        timeslots = Timeslot.objects.filter(schedule=schedule).order_by("begin_time")
        serializer = TimeslotSerializer(timeslots, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)




class TimeslotsCreateView(APIView):
    """
    Create multiple timeslots for a specific schedule.
    Example endpoint:
        POST /api/v1/timeslots/create/
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        schedule_id = request.data.get("schedule_id")
        start_time_str = request.data.get("start_time")
        end_time_str = request.data.get("end_time")
        duration = request.data.get("duration")
        break_duration = request.data.get("break_duration")

        if not all([schedule_id, start_time_str, end_time_str, duration, break_duration]):
            return Response(
                {"error": "Tous les paramètres (schedule_id, start_time, end_time, duration, break_duration) sont requis."},
                status=status.HTTP_400_BAD_REQUEST
            )

        schedule = get_object_or_404(Schedule, id=schedule_id)

        try:
            start_time = parse_datetime(start_time_str)
            end_time = parse_datetime(end_time_str)
            duration = int(duration)
            break_duration = int(break_duration)

            if start_time is None or end_time is None:
                raise ValueError("Les dates doivent être au format ISO 8601.")

        except (ValueError, TypeError) as e:
            return Response(
                {
                    "error_code": "INVALID_PARAMETERS",
                    "message": f"Paramètres invalides : {str(e)}"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        conflicting_timeslots = Timeslot.objects.filter(
            schedule=schedule
        ).filter(
            Q(begin_time__lt=end_time, end_time__gt=start_time)
        )

        if conflicting_timeslots.exists():
            conflict_serializer = TimeslotSerializer(conflicting_timeslots, many=True)
            return Response(
                {
                    "error_code": "TIMESLOT_CONFLICT",
                    "message": "Des timeslots existent déjà dans cette plage horaire.",
                    "conflicting_timeslots": conflict_serializer.data
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        current_start_time = start_time
        timeslots = []

        while current_start_time + timedelta(minutes=duration) <= end_time:
            current_end_time = current_start_time + timedelta(minutes=duration)

            timeslot = Timeslot(
                begin_time=current_start_time,
                end_time=current_end_time,
                schedule=schedule
            )
            timeslots.append(timeslot)

            current_start_time = current_end_time + timedelta(minutes=break_duration)

        if not timeslots:
            return Response(
                {"error": "Aucun timeslot valide n'a été généré avec les paramètres fournis."},
                status=status.HTTP_400_BAD_REQUEST
            )

        Timeslot.objects.bulk_create(timeslots)

        serializer = TimeslotSerializer(timeslots, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class AvailableTimeSlotView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        available_timeslots = Timeslot.objects.filter(
            schedule__uuid=kwargs["uuid"],
        ).annotate(
            has_registration=Exists(Registration.objects.filter(slot=OuterRef('pk')))
        ).filter(has_registration=False)

        serializer = TimeslotSerializer(available_timeslots, many=True)
        return Response(serializer.data)