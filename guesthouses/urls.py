from django.urls import path
from .views import (
    GuestHouseListView, GuestHouseDetailView, GuestHouseCreateView,
    GuestHouseUpdateView, OwnerGuestHouseListView, UpdateAvailabilityView
)

urlpatterns = [
    path("", GuestHouseListView.as_view(), name="guesthouse-list"),
    path("owner/", OwnerGuestHouseListView.as_view(), name="owner-guesthouse-list"),
    path("create/", GuestHouseCreateView.as_view(), name="guesthouse-create"),
    path("<int:pk>/", GuestHouseDetailView.as_view(), name="guesthouse-detail"),
    path("<int:pk>/update/", GuestHouseUpdateView.as_view(), name="guesthouse-update"),
    path("<int:pk>/availability/", UpdateAvailabilityView.as_view(), name="guesthouse-update-availability"),
]