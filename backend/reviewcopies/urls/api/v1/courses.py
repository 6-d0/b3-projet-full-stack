from django.urls import path

from reviewcopies.views.courses import (course_by_teacher_and_branch_view,
                                        course_list_view, create_course_view,
                                        teacher_course_list_view)

urlpatterns = [
    path("branch/<int:branch_id>/courses/", course_list_view, name="course-list"),
    path("<uuid:uuid>/courses/", teacher_course_list_view, name="teacher-course-list"),
    path(
        "<uuid:uuid>/<str:branch>/",
        course_by_teacher_and_branch_view,
        name="course-by-teacher-and-branch-view",
    ),
    path("create/", create_course_view, name="create-course"),
]
