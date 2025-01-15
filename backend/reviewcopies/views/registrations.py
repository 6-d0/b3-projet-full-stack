from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from reviewcopies.models import Registration, Course, Timeslot
from reviewcopies.serializers.registrations import RegistrationSerializer, AddRegistrationSerializer
from rest_framework.permissions import IsAuthenticated


class UserRegistrationsView(APIView):
    """
    Get all registrations
    """
    def get(self, request):
        registrations = Registration.objects.all()
        serializer = RegistrationSerializer(registrations, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class AddRegistrationView(APIView):
    """
    View to create a new registration
    """
    def post(self, request):
        """
        Create the registration with post method
        """
        print(request.data)
        course_id = request.data.get('course')
        slot_id = request.data.get('timeslot')

        if request.data.get('student') is None:
            student = request.user
        else:
            student = request.data.get('student')
        try:
            course = Course.objects.get(pk=course_id)
        except Course.DoesNotExist:
            return Response({"error": "Course not found"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            slot = Timeslot.objects.get(id=slot_id)
        except Timeslot.DoesNotExist:
            return Response({"error": "Timeslot not found"}, status=status.HTTP_400_BAD_REQUEST)

        if slot.schedule.session not in course.sessions.all():
            return Response({"error": "Timeslot does not belong to the course session"}, status=status.HTTP_400_BAD_REQUEST)

        registration_data = {
            'course': course.id,
            'student': student.id,
            'slot': slot.id,
            'comment': request.data.get('comment', ""),
        }

        serializer = AddRegistrationSerializer(data=registration_data, context={'request': request})

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
