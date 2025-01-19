from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from reviewcopies import models
from reviewcopies.serializers.sessions import SessionListSerializer, CreateSessionSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


class SessionListView(ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = models.Session.objects.all()
    serializer_class = SessionListSerializer

class CreateSession(APIView):
    permission_classes = [IsAuthenticated] # ajouter admin aussi
    def post(self, request, *args, **kwargs):

        data = request.data
        name = data.get("name")

        data = {
            "name": name,
        }

        serializer = CreateSessionSerializer(data=data)

        if serializer.is_valid():
            session = serializer.save()

            courses = data.get('courses', [])
            if courses:
                session.courses.set(courses)

            session.save()

            return Response({
                "message": "Session created successfully.",
                "session": CreateSessionSerializer(session).data
            }, status=status.HTTP_201_CREATED)

        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DeleteSession(APIView):
    def delete(self, request, *args, **kwargs):
        slug = kwargs.get('slug')
        session = models.Session.objects.get(slug=slug)
        session.delete()
        return Response({"message": "Session deleted successfully."}, status=status.HTTP_200_OK)
session_list_view = SessionListView.as_view()
