from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.views import APIView
from .models import Management
from login.utils.decorators import jwt_required
from .serializers import ManagementSerializer
# Create your views here.

@method_decorator(csrf_exempt, name='dispatch')
@method_decorator(jwt_required, name='dispatch')
class ManagementView(APIView):
    @swagger_auto_schema(
        tags=["Management"],
        operation_summary="Listado de registros",
        responses={200: "Success"},
        security=[{'Bearer': []}])
    def get(self, request):
        try:
            management = Management.objects.all()
            if not management:
                return JsonResponse({'data': [], 'success': True}, status=200)
            serializer = ManagementSerializer(management, many=True)
            return JsonResponse({'data': serializer.data, 'success': True}, status=200, safe=False)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    @swagger_auto_schema(
        tags=["Management"],
        operation_summary="Creación de registro",
        responses={201: "Registro creado"},
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'title': openapi.Schema(type=openapi.TYPE_STRING, description='Título del registro'),
                'description': openapi.Schema(type=openapi.TYPE_STRING, description='Descripción del registro'),
                'status': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='Estado del registro')
            }
        ),
        security=[{'Bearer': []}]
    )
    def post(self, request):
        try:
            serializer = ManagementSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse({'data': serializer.data, 'success': True}, status=201)
            return JsonResponse({'error': serializer.errors, 'success': False}, status=200)
        except Exception as e:
            return JsonResponse({'error': str(e), 'success': False}, status=500)


@method_decorator(csrf_exempt, name='dispatch')
@method_decorator(jwt_required, name='dispatch')
class ManagementWithIdView(APIView):
    @swagger_auto_schema(
        tags=["Management"],
        operation_summary="Actualización de registro",
        responses={200: "Registro actualizado", 404: "No encontrado"},
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'title': openapi.Schema(type=openapi.TYPE_STRING, description='Título del registro'),
                'description': openapi.Schema(type=openapi.TYPE_STRING, description='Descripción del registro'),
                'status': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='Estado del registro')
            }
        ),
        manual_parameters=[
            openapi.Parameter('id', openapi.IN_PATH, type=openapi.TYPE_INTEGER, description='ID del registro')
        ],
        security=[{'Bearer': []}]
    )
    def put(self, request, id):
        try:
            management = Management.objects.get(id=id)
            serializer = ManagementSerializer(management, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse({'data': serializer.data, 'success': True}, status=200)
            return JsonResponse({'error': serializer.errors, 'success': False}, status=200)
        except Management.DoesNotExist:
            return JsonResponse({'error': 'No se encontró el registro a actualizar', 'success': False}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    @swagger_auto_schema(
        tags=["Management"],
        operation_summary="Eliminación de registro",
        responses={204: "Registro eliminado", 404: "No encontrado"},
        manual_parameters=[
            openapi.Parameter('id', openapi.IN_PATH, type=openapi.TYPE_INTEGER, description='ID del registro')
        ],
        security=[{'Bearer': []}]
    )
    def delete(self, request, id):
        try:
            management = Management.objects.get(id=id)
            management.delete()
            return JsonResponse({'success': True}, status=200)
        except Management.DoesNotExist:
            return JsonResponse({'error': 'No se encontró el registro a eliminar', 'success': False}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
