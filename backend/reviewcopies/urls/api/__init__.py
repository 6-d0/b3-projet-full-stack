from django.urls import include, path

urlpatterns = [
    path("v1/", include("reviewcopies.urls.api.v1")),
]
