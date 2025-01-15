from django.urls import path
from reviewcopies.views.registrations import UserRegistrationsView, AddRegistrationView

urlpatterns = [
    path('add/', AddRegistrationView.as_view(), name='add-registrations'),
    path('', UserRegistrationsView.as_view(), name='user-registrations'),
]
