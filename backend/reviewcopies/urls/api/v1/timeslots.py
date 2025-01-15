from django.urls import path
from reviewcopies.views.timeslots import TimeslotsByScheduleView, TimeslotsCreateView, TimeslotsByScheduleUuidView

urlpatterns = [
    path('<int:schedule_id>/', TimeslotsByScheduleView.as_view(), name='timeslots-by-schedule'),
    path('<uuid:uuid>/', TimeslotsByScheduleUuidView.as_view(), name='timeslots-by-schedule-uuid'),
    path('create/', TimeslotsCreateView.as_view(), name='timeslots_create'),
]
