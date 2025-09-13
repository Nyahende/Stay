# from rest_framework import generics, permissions
# from .models import Booking
# from .serializers import BookingSerializer

# # Guest creates a booking
# class BookingCreateView(generics.CreateAPIView):
#     serializer_class = BookingSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     def perform_create(self, serializer):
#         serializer.save(guest=self.request.user, status="pending")

# # Guest sees their bookings
# class BookingListView(generics.ListAPIView):
#     serializer_class = BookingSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     def get_queryset(self):
#         return Booking.objects.filter(guest=self.request.user)

# # Owner sees bookings for their guesthouses
# class OwnerBookingListView(generics.ListAPIView):
#     serializer_class = BookingSerializer
#     permission_classes = [permissions.IsAuthenticated]

#     def get_queryset(self):
#         return Booking.objects.filter(guesthouse__owner=self.request.user)
