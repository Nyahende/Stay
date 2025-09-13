from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import GuestHouse
from .serializers import GuestHouseSerializer
import logging

logger = logging.getLogger(__name__)

class GuestHouseListView(APIView):
    def get(self, request):
        region = request.query_params.get('region')
        min_price = request.query_params.get('min_price')
        max_price = request.query_params.get('max_price')
        search = request.query_params.get('search')

        guest_houses = GuestHouse.objects.all()

        if region:
            guest_houses = guest_houses.filter(region=region)
        if min_price:
            guest_houses = guest_houses.filter(price_per_night__gte=min_price)
        if max_price:
            guest_houses = guest_houses.filter(price_per_night__lte=max_price)
        if search:
            guest_houses = guest_houses.filter(name__icontains=search)

        serializer = GuestHouseSerializer(guest_houses, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class GuestHouseCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if request.user.role != 'owner':
            logger.error(f"Unauthorized guest house creation attempt by user {request.user.username}")
            return Response({'error': 'Only owners can add guest houses'}, status=status.HTTP_403_FORBIDDEN)

        data = request.data.copy()
        data['owner'] = request.user.id
        serializer = GuestHouseSerializer(data=data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Guest house created successfully'}, status=status.HTTP_201_CREATED)
        logger.error(f"Guest house creation failed: {serializer.errors}")
        return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)