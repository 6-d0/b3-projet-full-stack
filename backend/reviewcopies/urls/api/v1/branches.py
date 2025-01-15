import reviewcopies.views.branches as views
from django.urls import path

urlpatterns = [
    path(
        "<slug:session>/",
        views.branch_list_view,
        name="branch-list",
    ),
]
