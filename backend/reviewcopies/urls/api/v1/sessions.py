import reviewcopies.views.sessions as views
from django.urls import path

urlpatterns = [
    path(
        "",
        views.session_list_view,
        name="session-list",
    ),
]
