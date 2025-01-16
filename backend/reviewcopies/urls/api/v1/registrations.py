from django.urls import path
from reviewcopies.views.registrations import UserRegistrationsView, AddRegistrationView, AllRegistrationsView

urlpatterns = [
    path('add/', AddRegistrationView.as_view(), name='add-registrations'),
    path('my-registrations/', UserRegistrationsView.as_view(), name='user-registration'),
    path('', AllRegistrationsView.as_view(), name='all-registrations'),
]
