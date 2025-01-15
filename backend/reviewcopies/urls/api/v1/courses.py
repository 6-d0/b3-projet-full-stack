from django.urls import path
from reviewcopies.views.courses import course_list_view,teacher_course_list_view

urlpatterns = [
    path("branch/<int:branch_id>/courses/", course_list_view, name="course-list"),
    path('<uuid:uuid>/courses/', teacher_course_list_view, name='teacher-course-list'),
]
