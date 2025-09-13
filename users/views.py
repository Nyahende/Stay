from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from django.http import JsonResponse
from django.middleware.csrf import get_token
import logging

# Set up logging
logger = logging.getLogger(__name__)

class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Registration successful'}, status=status.HTTP_201_CREATED)
        logger.error(f"Registration failed: {serializer.errors}, Request data: {request.data}")
        return Response({
            'error': serializer.errors,
            'request_data': request.data
        }, status=status.HTTP_400_BAD_REQUEST)

class MyTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        logger.debug(f"Login attempt: {request.data}")
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            return Response({
                'success': True,
                'access': response.data['access'],
                'refresh': response.data['refresh']
            })
        logger.error(f"Login failed: {response.data.get('detail', 'Invalid credentials')}, Request data: {request.data}")
        return Response({'success': False, 'error': response.data.get('detail', 'Invalid credentials')}, status=response.status_code)

class ProfileView(APIView):
    def get(self, request):
        user = request.user
        if user.is_authenticated:
            return Response({
                'username': user.username,
                'email': user.email
            })
        return Response({'error': 'Not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)

def get_csrf_token(request):
    return JsonResponse({'csrfToken': get_token(request)})