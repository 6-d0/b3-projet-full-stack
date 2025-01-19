from django.shortcuts import get_object_or_404
from django.utils.timezone import now
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from reviewcopies.permissions import IsTeacher
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
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

class CreateCourseView(APIView):
    permission_classes = [IsAuthenticated, IsTeacher]
    def post(self, request, *args, **kwargs):
        teacher = request.user
        name = request.data.get("name")
        if name is None:
            return Response({"error": "Name is required"}, status=400)
        session_slug = request.data.get("session")
        branch_slug = request.data.get("branch")
        if session_slug is None or branch_slug is None:
            return Response({"error": "Session and Branch are required"}, status=400)
        branch = models.Branch.objects.get(slug=branch_slug)
        session = models.Session.objects.get(slug=session_slug)
        course = models.Course.objects.create(name=name, teacher=teacher)
        branch.courses.add(course)
        session.courses.add(course)
        return Response({
            "message": "Course created successfully",
            "course": CourseListSerializer(course).data
        })

create_course_view = CreateCourseView.as_view()

class CourseByTeacherAndBranchs(APIView):
    def get(self, request, *args, **kwargs):
        teacher_id = self.kwargs.get("uuid")
        branch_slug = self.kwargs.get("branch")
        teacher = get_object_or_404(models.User, uuid=teacher_id)
        branch = get_object_or_404(models.Branch, slug=branch_slug)
        courses = branch.courses.filter(teacher=teacher)
        serializer = CourseListSerializer(courses, many=True)
        return Response(serializer.data)
course_by_teacher_and_branch_view = CourseByTeacherAndBranchs.as_view()
