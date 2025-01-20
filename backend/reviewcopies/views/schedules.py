import logging

from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from reviewcopies.models import Branch, Course, Schedule, Session, User
from reviewcopies.permissions import IsStudent, IsTeacher
from reviewcopies.serializers.schedules import (ScheduleCreateSerializer,
                                                ScheduleListSerializer)


class ScheduleListView(ListAPIView):
    """
    list all schedule of a specific session + branches
    """

    serializer_class = ScheduleListSerializer

    def get_object(self, key):
        match key:
            case "session":
                print(f"Session found: {self.kwargs['session']}")
                return get_object_or_404(Session, slug=self.kwargs["session"])
            case "branch":
                print(f"Session found: {self.kwargs['branch']}")
                return get_object_or_404(Branch, slug=self.kwargs["branch"])

    def get_queryset(self):
        session = self.get_object("session")
        branch = self.get_object("branch")
        schedules = Schedule.objects.filter(session=session)

        teacher_courses = Course.objects.filter(sessions=session, branches=branch)

        schedules = schedules.filter(teacher__courses__in=teacher_courses)

        return set(schedules)

    def get_serializer_context(self):
        return super().get_serializer_context() | {"branch": self.get_object("branch")}


schedule_list_view = ScheduleListView.as_view()


logger = logging.getLogger(__name__)


class ScheduleByUUID(APIView):
    """
    return as schedule with uuid
    """

    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        schedule = get_object_or_404(Schedule, uuid=kwargs["uuid"])
        serializer = ScheduleListSerializer(schedule)
        return Response(serializer.data)


class DeleteSchedule(APIView):
    """
    delete a schedule
    """

    def get(self, request, *args, **kwargs):
        schedule = get_object_or_404(Schedule, uuid=kwargs["uuid"])
        schedule.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class TeacherSchedulesView(APIView):
    """
    retrieve teacher schedules
    """

    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        if not "uuid" in kwargs.keys():
            teacher = request.user
        else:
            teacher = get_object_or_404(User, uuid=kwargs["uuid"])

        branch = request.GET.get("branch", None)
        schedules = Schedule.objects.filter(teacher=teacher).order_by("date")
        serializer = ScheduleListSerializer(
            schedules, many=True, context={"branch": branch}
        )

        return Response(serializer.data)


class CreateScheduleView(APIView):
    """
    create a new schedules
    """

    permission_classes = [IsAuthenticated, IsTeacher]

    def post(self, request, *args, **kwargs):
        serializer = ScheduleCreateSerializer(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            schedule = serializer.save()
            return Response(
                ScheduleListSerializer(schedule).data, status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdateCanSubscribeStatusView(APIView):
    """
    Permet de définir can_subscribe sur true ou false.
    Si can_subscribe est false, can_subscribe_until est mis à null.
    """

    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        schedule_id = kwargs.get("id")
        schedule = get_object_or_404(Schedule, id=schedule_id)

        if schedule.teacher != request.user:
            return Response(
                {"error": "Not authorized."}, status=status.HTTP_403_FORBIDDEN
            )

        can_subscribe = request.data.get("canSubscribe", None)

        if can_subscribe is None:
            return Response(
                {"error": "'canSubscribe' is required and must be a boolean value."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not isinstance(can_subscribe, bool):
            return Response(
                {"error": "'canSubscribe' must be a boolean value."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        schedule.can_subscribe = can_subscribe

        if not can_subscribe:
            schedule.can_subscribe_until = None

        schedule.save()

        return Response(
            {
                "message": "canSubscribe updated successfully.",
                "canSubscribe": schedule.can_subscribe,
                "canSubscribeUntil": schedule.can_subscribe_until,
            },
            status=status.HTTP_200_OK,
        )


class UpdateCanSubscribeUntilView(APIView):
    """
    Permet de modifier uniquement la date de can_subscribe_until.
    """

    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        schedule_id = kwargs.get("id")
        schedule = get_object_or_404(Schedule, id=schedule_id)

        if schedule.teacher != request.user:
            return Response(
                {"error": "Not authorized."}, status=status.HTTP_403_FORBIDDEN
            )

        can_subscribe_until = request.data.get("canSubscribeUntil", None)

        if can_subscribe_until == "":
            can_subscribe_until = None

        schedule.can_subscribe_until = can_subscribe_until
        schedule.save()

        return Response(
            {
                "message": "canSubscribeUntil updated successfully.",
                "canSubscribeUntil": schedule.can_subscribe_until,
            },
            status=status.HTTP_200_OK,
        )


class RetrieveScheduleView(APIView):
    """
    Permet de récupérer un planning (Schedule) par son identifiant (pk).
    Seul le professeur associé peut voir les détails du planning.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        schedule_id = kwargs.get("id")
        schedule = get_object_or_404(Schedule, id=schedule_id)

        if schedule.teacher != request.user:
            return Response(
                {"error": "Not authorized."}, status=status.HTTP_403_FORBIDDEN
            )

        serializer = ScheduleListSerializer(schedule)

        return Response(serializer.data, status=status.HTTP_200_OK)
