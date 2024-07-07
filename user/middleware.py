from rest_framework import status
from rest_framework.renderers import JSONRenderer
from django.conf import settings
import jwt
from rest_framework.response import Response


class JWTMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        # List of URLs or methods that should skip token validation
        excluded_urls = ['/user/login', '/user/register_user', '/swagger/', '/redoc/', '/api/token/refresh/', 'api/token/',
                         '/admin/']  # Adjust as needed

        if request.path_info in excluded_urls:
            return None  # Skip token validation for excluded URLs

        if not request.user.is_authenticated:
            try:
                token = request.COOKIES.get(settings.JWT_COOKIE_NAME)
                user_id = request.META.get('HTTP_USER_ID')
                if token:
                    payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
                    if not user_id:
                        response = Response({'error': 'user_id required'}, status=status.HTTP_401_UNAUTHORIZED)
                        response.accepted_renderer = JSONRenderer()
                        response.accepted_media_type = 'application/json'
                        response.renderer_context = {}
                        response.render()
                        return response
                    elif user_id != payload['user_id']:
                        response = Response({'error': 'Invalid token'}, status=status.HTTP_401_UNAUTHORIZED)
                        response.accepted_renderer = JSONRenderer()
                        response.accepted_media_type = 'application/json'
                        response.renderer_context = {}
                        response.render()
                        return response
                else:
                    response = Response({'error': 'User Logged Out'}, status=status.HTTP_400_BAD_REQUEST)
                    response.accepted_renderer = JSONRenderer()
                    response.accepted_media_type = 'application/json'
                    response.renderer_context = {}
                    response.render()
                    return response
            except jwt.ExpiredSignatureError:
                response = Response({'error': 'Token expired'}, status=status.HTTP_401_UNAUTHORIZED)
                response.accepted_renderer = JSONRenderer()
                response.accepted_media_type = 'application/json'
                response.renderer_context = {}
                response.render()
                return response
            except jwt.DecodeError as e:
                response = Response({'error': str(e)}, status=status.HTTP_401_UNAUTHORIZED)
                response.accepted_renderer = JSONRenderer()
                response.accepted_media_type = 'application/json'
                response.renderer_context = {}
                response.render()
                return response
            except Exception as e:
                response = Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
                response.accepted_renderer = JSONRenderer()
                response.accepted_media_type = 'application/json'
                response.renderer_context = {}
                response.render()
                return response

        return None
