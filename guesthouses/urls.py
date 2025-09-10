from django.urls import path
from .views import GuestHouseListView, GuestHouseDetailView, GuestHouseCreateView, GuestHouseUpdateView

urlpatterns = [
    path("", GuestHouseListView.as_view(), name="guesthouse-list"),
    path("<int:pk>/", GuestHouseDetailView.as_view(), name="guesthouse-detail"),
    path("create/", GuestHouseCreateView.as_view(), name="guesthouse-create"),
    path("<int:pk>/update/", GuestHouseUpdateView.as_view(), name="guesthouse-update"),
]
