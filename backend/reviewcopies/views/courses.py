from django.shortcuts import get_object_or_404
from django.utils.timezone import now
from rest_framework.generics import ListAPIView
from reviewcopies import models
from reviewcopies.serializers.courses import CourseListSerializer

class CourseListView(ListAPIView):
    """
    List of all courses for a sessions and a branch
    """
    serializer_class = CourseListSerializer

    def get_queryset(self):
        branch_id = self.kwargs.get("branch_id")
        branch = get_object_or_404(models.Branch, id=branch_id)
        next_session = (
            models.Session.objects.filter(schedules__date__gte=now())
            .order_by("schedules__date")
            .first()
        )

        if not next_session:
            return models.Course.objects.none()
        queryset = models.Course.objects.filter(
            branches=branch,
            sessions=next_session
        ).distinct()

        return queryset

course_list_view = CourseListView.as_view()


class TeacherCourseListView(ListAPIView):
    """
    Retrieve all course for a specific teacher
    """
    serializer_class = CourseListSerializer

    def get_queryset(self):
        teacher_id = self.kwargs.get("uuid")
        teacher = get_object_or_404(models.User, uuid=teacher_id)
        queryset = models.Course.objects.filter(
            teacher=teacher
        ).distinct()

        return queryset

teacher_course_list_view = TeacherCourseListView.as_view()
