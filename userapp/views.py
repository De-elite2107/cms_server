from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import *
from .serializers import *
from rest_framework import status, generics
from rest_framework.parsers import MultiPartParser
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

# Create your views here.
class RegisterView(APIView):
    parser_classes = [MultiPartParser]
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