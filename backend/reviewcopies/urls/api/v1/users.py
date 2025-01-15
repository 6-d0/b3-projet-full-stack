from django.urls import path

import reviewcopies.views.users as views

urlpatterns = [
    path(
        "details/",
        views.user_detail_view,
        name="user-detail",
    ),
]
