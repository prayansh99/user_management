from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import User, CustomModelException
from functools import wraps
import jwt
import datetime
from django.conf import settings
from .serializers import UserSerializer
import hashlib


class SignupView(APIView):

    @swagger_auto_schema(
        operation_id='register_user',
        operation_description="Register a new user",
        request_body=UserSerializer,
        responses={
            201: openapi.Response("User created successfully"),
            400: openapi.Response("Bad Request")
        }
    )
    def post(self, request):
        if not request.data:  # Check if request body is empty
            return Response({"error": "Request body cannot be empty"}, status=status.HTTP_400_BAD_REQUEST)
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            if User.find_by_email(data['email']) or User.find_by_username(data['username']):
                return Response({"error": "User with this email or username already exists."},
                                status=status.HTTP_400_BAD_REQUEST)
            data['password'] = hashlib.sha256(data['password'].encode('utf-8')).hexdigest()
            User.create_user(data)
            return Response({"message": "User created successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    @swagger_auto_schema(
        operation_id='login',
        operation_description="Login a user",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'email': openapi.Schema(type=openapi.TYPE_STRING, description='User email'),
                'password': openapi.Schema(type=openapi.TYPE_STRING, description='User password'),
            }
        ),
        responses={
            200: openapi.Response("Login successful, returns tokens"),
            401: openapi.Response("Invalid credentials")
        }
    )
    def post(self, request):
        if not request.data:  # Check if request body is empty
            return Response({"error": "Request body cannot be empty"}, status=status.HTTP_400_BAD_REQUEST)
        data = request.data
        user = User.find_by_email(data['email'])
        if user and user.get('password') == hashlib.sha256(data['password'].encode('utf-8')).hexdigest():
            user_id = str(user['_id'])  # Convert ObjectId to string if needed
            user['_id'] = str(user['_id'])

            # Retrieve or create Django user instance based on email or username
            # try:
            #     django_user = DjangoUser.objects.get(email=user['email'])
            # except DjangoUser.DoesNotExist:
            #     django_user = DjangoUser.objects.create_user(username=user['username'], email=user['email'])
            payload = {
                'user_id': str(user['_id']),
                'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=settings.JWT_EXPIRATION),
            }
            access_token = jwt.encode(payload, settings.SECRET_KEY)

            response = Response({
                'access': access_token,
                'user_id': user_id
            }, status=status.HTTP_200_OK)
            response.set_cookie(settings.JWT_COOKIE_NAME, access_token, max_age=settings.JWT_EXPIRATION, httponly=True)
            return response
        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)


class LogoutView(APIView):
    # permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_id='logout',
        operation_description="Logout a user",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'refresh_token': openapi.Schema(type=openapi.TYPE_STRING, description='Refresh token to blacklist')
            }
        ),
        responses={
            200: openapi.Response("Successfully logged out"),
            400: openapi.Response("Bad Request")
        }
    )
    def post(self, request):

        try:
            response = Response({"message": "Successfully logged out"}, status=status.HTTP_200_OK)
            response.delete_cookie(settings.JWT_COOKIE_NAME)
            return response
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class UserDetailView(APIView):
    # permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_id='user_profile',
        operation_description="Get user details by user ID",
        manual_parameters=[
            openapi.Parameter('user_id', openapi.IN_PATH, description="ID of the user", type=openapi.TYPE_STRING)
        ],
        responses={
            200: openapi.Response("User details retrieved successfully"),
            400: openapi.Response("User not found"),
            400: openapi.Response("Invalid request")
        }
    )
    def get(self, request, user_id=None):
        if user_id:
            if not user_id.isalnum():
                return Response({"error": "Invalid user_id"}, status=status.HTTP_400_BAD_REQUEST)
            try:
                user = User.find_by_id(user_id)
            except CustomModelException as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": "Invalid request"}, status=status.HTTP_400_BAD_REQUEST)
        if user:
            user['_id'] = str(user['_id'])
            return Response(user, status=status.HTTP_200_OK)
        return Response({"error": "User not found"}, status=status.HTTP_400_BAD_REQUEST)


class UserDetailByUsernameView(APIView):
    # permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_id='user_profile',
        operation_description="Get user details by username",
        manual_parameters=[
            openapi.Parameter('username', openapi.IN_PATH, description="Username of the user", type=openapi.TYPE_STRING)
        ],
        responses={
            200: openapi.Response("User details retrieved successfully"),
            400: openapi.Response("User not found"),
            400: openapi.Response("Invalid request")
        }
    )
    def get(self, request, username=None):
        if username:
            if not username.isalnum():
                return Response({"error": "Invalid username"}, status=status.HTTP_400_BAD_REQUEST)
            user = User.find_by_username(username)
        else:
            return Response({"error": "Invalid request"}, status=status.HTTP_400_BAD_REQUEST)

        if user:
            user['_id'] = str(user['_id'])
            return Response(user, status=status.HTTP_200_OK)
        return Response({"error": "User not found"}, status=status.HTTP_400_BAD_REQUEST)


def handle_errors(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            # Handle other types of exceptions
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return wrapper
