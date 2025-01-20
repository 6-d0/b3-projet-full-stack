import reviewcopies.views.sessions as views
from django.urls import path

urlpatterns = [
    path(
        "<slug:slug>/courses/",
        views.DeleteCourseFromSession.as_view(),
        name="session-list",
    ),
    path(
        "<slug:slug>/delete/",
        views.DeleteSession.as_view(),
        name="session-list",
    ),
    path(
        "",
        views.session_list_view,
        name="session-list",
    ),
    path(
        "create/",
        views.CreateSession.as_view(),
        name="create-session",
    ),
]
