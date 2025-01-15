from rest_framework.generics import ListAPIView
from reviewcopies import models
from reviewcopies.serializers.sessions import SessionListSerializer
from rest_framework.permissions import IsAuthenticated
from reviewcopies.permissions import IsStudent

class SessionListView(ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = models.Session.objects.registrables()
    serializer_class = SessionListSerializer


session_list_view = SessionListView.as_view()
