from rest_framework.generics import RetrieveAPIView

from reviewcopies import models
from reviewcopies.serializers.users import UserDetailSerializer


class UserDetailView(RetrieveAPIView):
    serializer_class = UserDetailSerializer
    model = models.User

    def get_object(self):
        return self.request.user


user_detail_view = UserDetailView.as_view()
