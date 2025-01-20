import reviewcopies.views.branches as views
from django.urls import path

urlpatterns = [
    path(
        "",
        views.branch_view,
        name="branch-view"
    ),
    path(
        "create/",
        views.create_branch_view,
        name="branch-list",
    ),
    path(
        "<slug:session>/",
        views.branch_list_view,
        name="branch-list",
    ),
]
