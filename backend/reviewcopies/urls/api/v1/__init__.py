from django.urls import include, path

urlpatterns = [
    path("auth/", include("reviewcopies.urls.api.v1.auth")),
    path("sessions/", include("reviewcopies.urls.api.v1.sessions")),
    path("branches/", include("reviewcopies.urls.api.v1.branches")),
    path("schedules/", include("reviewcopies.urls.api.v1.schedules")),
    path("user/", include("reviewcopies.urls.api.v1.users")),
    path("registrations/", include("reviewcopies.urls.api.v1.registrations")),
    path("timeslots/",include("reviewcopies.urls.api.v1.timeslots")),
    path("courses/", include("reviewcopies.urls.api.v1.courses")),
    path("student/", include("reviewcopies.urls.api.v1.test"))
]
