from django.urls import include, path

app_name = "reviewcopies"

urlpatterns = [
    path("admin/", include("reviewcopies.urls.admin")),
    path("auth/", include("reviewcopies.urls.auth")),
    path("api/", include("reviewcopies.urls.api")),
]
