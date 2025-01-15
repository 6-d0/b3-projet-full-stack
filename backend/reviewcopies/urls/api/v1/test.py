from django.urls import path
from reviewcopies.views.test import StudentOnlyView

urlpatterns = [
    path('student-only/', StudentOnlyView.as_view(), name='student_only'),
]
