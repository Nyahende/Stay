from rest_framework import generics, permissions
from .models import GuestHouse
from .serializers import GuestHouseSerializer

# List all guesthouses (for guests)
from rest_framework import generics, permissions
from .models import GuestHouse
from .serializers import GuestHouseSerializer

class GuestHouseListView(generics.ListAPIView):
    serializer_class = GuestHouseSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        queryset = GuestHouse.objects.all()
        region = self.request.query_params.get("region")
        min_price = self.request.query_params.get("min_price")
        max_price = self.request.query_params.get("max_price")
        amenities = self.request.query_params.get("amenities")  # comma-separated

        if region:
            queryset = queryset.filter(region__iexact=region)

        if min_price:
            queryset = queryset.filter(price_per_night__gte=min_price)

        if max_price:
            queryset = queryset.filter(price_per_night__lte=max_price)

        if amenities:
            amenities_list = [a.strip().lower() for a in amenities.split(",")]
            # Filter guesthouses containing ALL requested amenities
            for amenity in amenities_list:
                queryset = queryset.filter(amenities__icontains=amenity)

        return queryset



# Retrieve a single guesthouse detail
class GuestHouseDetailView(generics.RetrieveAPIView):
    queryset = GuestHouse.objects.all()
    serializer_class = GuestHouseSerializer
    permission_classes = [permissions.AllowAny]

# Owner can create a guesthouse
class GuestHouseCreateView(generics.CreateAPIView):
    serializer_class = GuestHouseSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

# Owner can update their guesthouse
class GuestHouseUpdateView(generics.RetrieveUpdateAPIView):
    queryset = GuestHouse.objects.all()
    serializer_class = GuestHouseSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Only allow owners to update their guesthouses
        return self.queryset.filter(owner=self.request.user)


from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets

class GuestHouseViewSet(viewsets.ModelViewSet):
    queryset = GuestHouse.objects.all()
    serializer_class = GuestHouseSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Owners can see only their guesthouses for updates
        return self.queryset.filter(owner=self.request.user)

    @action(detail=True, methods=["PATCH"])
    def update_availability(self, request, pk=None):
        guesthouse = self.get_object()
        status_value = request.data.get("availability_status")
        if status_value not in ["available", "few", "full"]:
            return Response({"error": "Invalid availability status."}, status=status.HTTP_400_BAD_REQUEST)
        guesthouse.availability_status = status_value
        guesthouse.save()
        return Response({"success": f"Availability updated to {status_value}"})
