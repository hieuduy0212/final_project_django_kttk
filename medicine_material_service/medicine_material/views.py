from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Medicine, MedicineCategory, MedicineSupplier, Material, MaterialType, MaterialSupplier
from .serializers import MedicineSerializer, MedicineCategorySerializer, MedicineSupplierSerializer, MaterialSerializer, \
    MaterialTypeSerializer, MaterialSupplierSerializer
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import requests
import jwt
from django.conf import settings


# Utility function to fetch data from another service
def fetch_data_from_service(url, token):
    headers = {
        'Authorization': f'Bearer {token}'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return None


# Decorator to check JWT token
def jwt_required():
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            auth_header = request.headers.get('Authorization')
            if not auth_header:
                return Response({'error': 'Authorization header not found'}, status=401)
            try:
                token_type, token = auth_header.split(' ')
                if token_type != 'Bearer':
                    raise ValueError('Invalid token type')
            except (ValueError, IndexError):
                return Response({'error': 'Invalid authorization header'}, status=401)
            try:
                decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
                user_id = decoded_token['id']
            except jwt.ExpiredSignatureError:
                return Response({'error': 'JWT is expired'}, status=401)
            except jwt.InvalidTokenError:
                return Response({'error': 'Invalid JWT'}, status=401)
            kwargs['user_id'] = user_id
            return view_func(request, *args, **kwargs)

        return wrapper

    return decorator


# Medicine Supplier Views
class MedicineSupplierCreateView(APIView):
    # @method_decorator(jwt_required())
    # @csrf_exempt
    def post(self, request):
        serializer = MedicineSupplierSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        suppliers = MedicineSupplier.objects.all()
        serializer = MedicineSupplierSerializer(suppliers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

# Medicine Category Views
class MedicineCategoryCreateView(APIView):
    # @method_decorator(jwt_required())
    # @csrf_exempt
    def post(self, request):
        serializer = MedicineCategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        cates = MedicineCategory.objects.all()
        serializer = MedicineCategorySerializer(cates, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


# Medicine Views
class MedicineListView(APIView):
    # @method_decorator(jwt_required())
    def get(self, request):
        medicines = Medicine.objects.all()
        serializer = MedicineSerializer(medicines, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class MedicineDetailView(APIView):
    # @method_decorator(jwt_required())
    def get(self, request, user_id, medicine_id):
        try:
            medicine = Medicine.objects.get(id=medicine_id)
        except Medicine.DoesNotExist:
            return Response({'error': 'Medicine not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = MedicineSerializer(medicine)
        return Response(serializer.data, status=status.HTTP_200_OK)


class MedicineCreateView(APIView):
    # @method_decorator(jwt_required())
    # @csrf_exempt
    def post(self, request):
        serializer = MedicineSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MedicineUpdateView(APIView):
    # @method_decorator(jwt_required())
    # @csrf_exempt
    def put(self, request, user_id, medicine_id):
        try:
            medicine = Medicine.objects.get(id=medicine_id)
        except Medicine.DoesNotExist:
            return Response({'error': 'Medicine not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = MedicineSerializer(medicine, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MedicineDeleteView(APIView):
    # @method_decorator(jwt_required())
    # @csrf_exempt
    def delete(self, request, user_id, medicine_id):
        try:
            medicine = Medicine.objects.get(id=medicine_id)
        except Medicine.DoesNotExist:
            return Response({'error': 'Medicine not found'}, status=status.HTTP_404_NOT_FOUND)
        medicine.delete()
        return Response({'message': 'Medicine deleted successfully'}, status=status.HTTP_204_NO_CONTENT)


# Material Views
class MaterialListView(APIView):
    # @method_decorator(jwt_required())
    def get(self, request):
        materials = Material.objects.all()
        serializer = MaterialSerializer(materials, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class MaterialDetailView(APIView):
    # @method_decorator(jwt_required())
    def get(self, request, user_id, material_id):
        try:
            material = Material.objects.get(id=material_id)
        except Material.DoesNotExist:
            return Response({'error': 'Material not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = MaterialSerializer(material)
        return Response(serializer.data, status=status.HTTP_200_OK)


class MaterialCreateView(APIView):
    # @method_decorator(jwt_required())
    # @csrf_exempt
    def post(self, request):
        serializer = MaterialSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MaterialUpdateView(APIView):
    # @method_decorator(jwt_required())
    # @csrf_exempt
    def put(self, request, user_id, material_id):
        try:
            material = Material.objects.get(id=material_id)
        except Material.DoesNotExist:
            return Response({'error': 'Material not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = MaterialSerializer(material, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MaterialDeleteView(APIView):
    # @method_decorator(jwt_required())
    # @csrf_exempt
    def delete(self, request, user_id, material_id):
        try:
            material = Material.objects.get(id=material_id)
        except Material.DoesNotExist:
            return Response({'error': 'Material not found'}, status=status.HTTP_404_NOT_FOUND)
        material.delete()
        return Response({'message': 'Material deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
