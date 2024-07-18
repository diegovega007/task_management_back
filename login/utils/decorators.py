from functools import wraps
from django.http import JsonResponse
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.authentication import JWTAuthentication
from login.models import User

def jwt_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        auth = JWTAuthentication()
        auth_header = request.headers.get('Authorization')
        
        if auth_header is None:
            return JsonResponse({'error': 'Token no proporcionado', 'success': False}, status=401)
        
        try:
    
            validated_token = auth.get_validated_token(auth_header)
            user_id = validated_token.get('user_id')

            if not user_id:
                raise InvalidToken("El token no contiene user_id")

            user = User.objects.get(id=user_id)
            
            if user is None:
                raise InvalidToken("No se pudo autenticar el token")
            
            request.user = user
        except (InvalidToken, TokenError) as e:
            return JsonResponse({'error': 'Token inválido o expirado', 'success': False}, status=401)
        except IndexError:
            return JsonResponse({'error': 'Formato de token inválido', 'success': False}, status=401)
        except User.DoesNotExist:
            return JsonResponse({'error': 'Usuario no encontrado', 'success': False}, status=401)

        return view_func(request, *args, **kwargs)

    return _wrapped_view