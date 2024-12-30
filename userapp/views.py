from rest_framework import viewsets
from .models import User
from .models import *
from .serializers import *
from django.contrib.auth import authenticate, login
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from django.utils.translation import gettext as _
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

# Create your views here.
class RegisterView(APIView):
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('username', openapi.IN_FORM, description="Username of the user", type=openapi.TYPE_STRING, required=True),
            openapi.Parameter('first_name', openapi.IN_FORM, description="First name of the user", type=openapi.TYPE_STRING, required=True),
            openapi.Parameter('last_name', openapi.IN_FORM, description="Last name of the user", type=openapi.TYPE_STRING, required=True),
            openapi.Parameter('email', openapi.IN_FORM, description="Email address of the user", type=openapi.TYPE_STRING, required=True),
            openapi.Parameter('phone', openapi.IN_FORM, description="Phone number of the user", type=openapi.TYPE_STRING, required=True),
            openapi.Parameter('password', openapi.IN_FORM, description="Password for the user account", type=openapi.TYPE_STRING, required=True),
            openapi.Parameter('address', openapi.IN_FORM, description="Address of the user", type=openapi.TYPE_STRING, required=True),
            openapi.Parameter('dob', openapi.IN_FORM, description="Date of birth of the user (YYYY-MM-DD)", type=openapi.TYPE_STRING, required=True),
            openapi.Parameter('occupation', openapi.IN_FORM, description="Occupation of the user", type=openapi.TYPE_STRING, required=True),
            openapi.Parameter('wedding', openapi.IN_FORM, description="Wedding date of the user (YYYY-MM-DD)", type=openapi.TYPE_STRING),
            openapi.Parameter('role', openapi.IN_FORM, description="Role of the user", type=openapi.TYPE_STRING, required=True),
        ],
        responses={201: openapi.Response('User registered successfully', UserSerializer)}
    )
    def post(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                'message': 'User registered successfully',
                'data': {
                    'id': user.id,
                    'username': user.username,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'email': user.email,  # Include email if needed
                    'phone': user.phone,
                    'address': user.address,
                    'dob': user.dob,
                    'occupation': user.occupation,
                    'wedding': user.wedding,
                    'role': user.role,
                }
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        # Extract username and password from the request data
        username = request.data.get('username')
        password = request.data.get('password')

        # Authenticate user
        user = authenticate(username=username, password=password)

        if user is not None:
            # Get or create token for the authenticated user
            token, created = Token.objects.get_or_create(user=user)
            data = {
                'user_id': user.id,
                'username': user.username,
                'email': user.email,
                'role': getattr(user, 'role', None),  # Use getattr for safety in case role doesn't exist
            }
            # Return token and user information on successful login
            return Response({
                'token': token.key,
                'message': 'Login Successful',
                'data': data,
            })
        else:
            # Return an error response if authentication fails
            return Response({'error': 'Invalid Credentials'}, status=status.HTTP_400_BAD_REQUEST)

class CustomTokenAuthentication(BaseAuthentication):
    def authenticate(self, request):
        # Get the Authorization header
        auth_header = request.headers.get('Authorization')
        
        if not auth_header:
            return None  # No auth header provided

        try:
            # Split the header into type and token
            auth_type, token = auth_header.split()
            if auth_type.lower() != 'token':
                return None  # Not a Token type
            
            # Validate the token and retrieve the user
            user = self.get_user_from_token(token)
            return (user, token)  # Return user and token

        except ValueError:
            raise AuthenticationFailed('Invalid authorization header.')

    def get_user_from_token(self, token):
        try:
            # Retrieve the user associated with the token
            token_obj = Token.objects.get(key=token)
            return token_obj.user
        except Token.DoesNotExist:
            raise AuthenticationFailed('Invalid token.')
        
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]  # Ensure the user is authenticated
    authentication_classes = [CustomTokenAuthentication]  # Use your custom authentication

    def post(self, request):
        try:
            # Get the token from the request header
            token = request.auth
            
            if not token:
                return Response({'error': 'No token provided.'}, status=status.HTTP_400_BAD_REQUEST)

            # Delete the token to log out the user
            Token.objects.filter(key=token).delete()
            
            return Response({'message': 'Successfully logged out.'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)