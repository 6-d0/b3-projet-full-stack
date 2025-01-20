from django.urls import path

from reviewcopies.views.registrations import (AddRegistrationView, AllRegistrationsView,
                                              RegistrationByScheduleUUID,
                                              RegistrationByTimeSlot,
                                              UserRegistrationsView)

urlpatterns = [
    path(
        "<uuid:uuid>/",
        RegistrationByScheduleUUID.as_view(),
        name="registrations-by-schedule-uuid",
    ),
    path(
        "<uuid:uuid>/details/",
        RegistrationByTimeSlot.as_view(),
        name="registration-by-slot-uuid",
    ),
    path("add/", AddRegistrationView.as_view(), name="add-registrations"),
    path(
        "my-registrations/", UserRegistrationsView.as_view(), name="user-registration"
    ),
    path("", AllRegistrationsView.as_view(), name="all-registrations"),
]
