from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from login.utils.decorators import jwt_required
from django.utils.decorators import method_decorator
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import User
from rest_framework_simplejwt.tokens import RefreshToken

# Create your views here.

@method_decorator(csrf_exempt, name='dispatch')
class LoginView(APIView):
    @swagger_auto_schema(
        tags=["Login"],
        operation_summary="Login de usuario",
        responses={200: "Success"},
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING, description='Nombre de usuario'),
                'password': openapi.Schema(type=openapi.TYPE_STRING, description='Contraseña')
            }
        )
    )
    def post(self, request):
        try:
            # Usa request.data para obtener el cuerpo de la solicitud
            username = request.data.get('username')
            password = request.data.get('password')
            
            user = User.objects.filter(username=username).first()
            if not user or not user.validate_password(password):
                return JsonResponse({'error': 'Usuario o contraseña incorrecta', 'success': False}, status=200)
            refresh = RefreshToken.for_user(user)
            return JsonResponse({
                'success': True,
                'token': str(refresh.access_token),
                'refresh_token': str(refresh)
            }, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e), 'success': False}, status=500)
        
@method_decorator(csrf_exempt, name='dispatch')
class LogoutView(APIView):
    @swagger_auto_schema(
        tags=["Logout"],
        operation_summary="Logout de usuario",
        responses={200: "Success"},
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'refresh_token': openapi.Schema(type=openapi.TYPE_STRING, description='Token de refresco')
            }
        ),
    )
    def post(self, request):
        try:
            refresh = RefreshToken(request.data.get('refresh_token'))
            refresh.blacklist()
            return JsonResponse({'success': True}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e), 'success': False}, status=500)