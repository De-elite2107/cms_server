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
        request_body=UserSerializer,
        responses={200: openapi.Response('User registered successfully', UserSerializer)}
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
        return Response(serializer.errors, status=400)

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
            return Response({'error': 'Invalid Credentials'}, status=401)

class AdminLogin(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        username = request.data.get("username")
        password = request.data.get("password")
        
        # Authenticate the user
        user = authenticate(request, username=username, password=password)
        
        # Check if user is authenticated and has admin role
        if user is not None:
            # Get or create token for the authenticated user
            if user.is_staff:  # Check if the user is an admin
                token, created = Token.objects.get_or_create(user=user)
                data = {
                    'user_id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'role': getattr(user, 'role', None),  # Use getattr for safety in case role doesn't exist
                }
                return Response({
                    'token': token.key,
                    'message': 'Login Successful',
                    'data': data,
                })
            else:
                return Response({"success": False, "error": "User does not have admin privileges"}, status=403)
        else:
            return Response({"success": False, "error": "Invalid credentials"}, status=401)

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

    def post(self, request):
        try:
            # Get the token from the request header
            token = request.auth
            
            if not token:
                return Response({'error': 'No token provided.'}, status=400)

            # Delete the token to log out the user
            Token.objects.filter(key=token).delete()
            
            return Response({'message': 'Successfully logged out.'}, status=200)
        except Exception as e:
            return Response({'error': str(e)}, status=400)