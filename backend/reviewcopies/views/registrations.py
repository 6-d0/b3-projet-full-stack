from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from reviewcopies.models import Registration, Course, Timeslot, Schedule
from reviewcopies.serializers.registrations import RegistrationSerializer, AddRegistrationSerializer
from rest_framework.permissions import IsAuthenticated
from reviewcopies.permissions import IsStudent, IsTeacher


class AllRegistrationsView(APIView):
    """
    Get all registrations
    """
    def get(self, request):
        registrations = Registration.objects.all()
        serializer = RegistrationSerializer(registrations, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class UserRegistrationsView(APIView):
    """
    get registration linked to a user
    """
    permission_classes = [IsAuthenticated, IsStudent]
    def get(self, request):
        registrations = Registration.objects.filter(student=request.user)
        serializer = RegistrationSerializer(registrations, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class AddRegistrationView(APIView):
    """
    View to create a new registration
    """
    permission_classes = [IsAuthenticated]
    def post(self, request):
        """
        Create the registration with post method
        """
        print(request.data)
        course_slug = request.data.get('course')
        slot_uuid = request.data.get('timeslot')
        try:
            course = Course.objects.get(slug=course_slug)
        except Course.DoesNotExist:
            return Response({"error": "Course not found"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            slot = Timeslot.objects.get(uuid=slot_uuid)
        except Timeslot.DoesNotExist:
            return Response({"error": "Timeslot not found"}, status=status.HTTP_400_BAD_REQUEST)

        if slot.schedule.session not in course.sessions.all():
            return Response({"error": "Timeslot does not belong to the course session"}, status=status.HTTP_400_BAD_REQUEST)

        registration_data = {
            'course': course.id,
            'student': request.user.id,
            'slot': slot.id,
            'comment': request.data.get('comment', ""),
        }

        serializer = AddRegistrationSerializer(data=registration_data, context={'request': request})

        if serializer.is_valid() and serializer.validate(registration_data):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RegistrationByTimeSlot(APIView):
    permission_classes = [IsTeacher, IsAuthenticated]
    def get(self, request, *args, **kwargs):
        uuid = kwargs.pop("uuid")
        try:
            slot = Timeslot.objects.filter(uuid=uuid).first()
            registration = Registration.objects.filter(slot=slot).first()
            serializer = RegistrationSerializer(registration)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Timeslot.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

class RegistrationByScheduleUUID(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
        uuid = kwargs.pop("uuid")
        try:
            schedule = Schedule.objects.get(uuid=uuid)
            registration = Registration.objects.filter(slot__schedule=schedule)
            serializer = RegistrationSerializer(registration, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Timeslot.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
