# from django.db import models
# # from users.models import User
# from guesthouses.models import GuestHouse

# class Booking(models.Model):
#     STATUS_CHOICES = [
#         ("pending", "Pending"),
#         ("confirmed", "Confirmed"),
#         ("cancelled", "Cancelled"),
#     ]

#     guest = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bookings")
#     guesthouse = models.ForeignKey(GuestHouse, on_delete=models.CASCADE, related_name="bookings")
#     check_in = models.DateField()
#     check_out = models.DateField()
#     status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"Booking by {self.guest.username} at {self.guesthouse.name}"
