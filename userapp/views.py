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
    @swagger_auto_schema(
        request_body=UserSerializer,
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
