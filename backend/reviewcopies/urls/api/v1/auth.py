from django.contrib.auth import login
from django.urls import path
from knox import views as knox_views
from knox.views import LoginView as KnoxLoginView
from rest_framework import permissions
from rest_framework.authtoken.serializers import AuthTokenSerializer


class LoginView(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        if "e" in str(user.username):
            user.role = "student"
        elif "h" in str(user.username):
            user.role = "teacher"
        else:
            user.role = "admin"
        user.save(update_fields=["role"])
        login(request, user)
        return super(LoginView, self).post(request, format=None)


urlpatterns = [
    path("login/", LoginView.as_view(), name="knox_login"),
    path("logout/", knox_views.LogoutView.as_view(), name="knox_logout"),
    path("logoutall/", knox_views.LogoutAllView.as_view(), name="knox_logoutall"),
]
