from django.urls import path

import reviewcopies.views.schedules as views

urlpatterns = [
    path("<uuid:uuid>/", views.ScheduleByUUID.as_view(), name="schedule-by-uuid"),
    path("delete/<uuid:uuid>/", views.DeleteSchedule.as_view(), name="delete-schedule"),
    path(
        "retrieve-schedule/<int:id>/",
        views.RetrieveScheduleView.as_view(),
        name="retrieve-schedule",
    ),
    path(
        "teacher-schedules/<uuid:uuid>/",
        views.TeacherSchedulesView.as_view(),
        name="teacher-schedules",
    ),
    path(
        "update-can-subscribe/<int:id>/",
        views.UpdateCanSubscribeStatusView.as_view(),
        name="update-can-subscribe",
    ),
    path(
        "update-can-subscribe-until/<int:id>/",
        views.UpdateCanSubscribeUntilView.as_view(),
        name="update-can-subscribe-until",
    ),
    path(
        "<slug:session>/<slug:branch>/",
        views.schedule_list_view,
        name="schedule-list",
    ),
    path(
        "teacher-schedules/",
        views.TeacherSchedulesView.as_view(),
        name="teacher-schedules",
    ),
    path(
        "create-schedule/",
        views.CreateScheduleView.as_view(),
        name="create-schedule",
    ),
]
