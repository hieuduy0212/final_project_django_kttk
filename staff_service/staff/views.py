from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Staff, Role
from .serializers import StaffSerializer, RoleSerializer
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


class StaffListView(APIView):
    @method_decorator(jwt_required())
    def get(self, request, user_id):
        staffs = Staff.objects.all()
        serializer = StaffSerializer(staffs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class StaffDetailView(APIView):
    @method_decorator(jwt_required())
    def get(self, request, user_id, staff_id):
        try:
            staff = Staff.objects.get(id=staff_id)
        except Staff.DoesNotExist:
            return Response({'error': 'Staff not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = StaffSerializer(staff)
        return Response(serializer.data, status=status.HTTP_200_OK)


class StaffCreateView(APIView):
    @method_decorator(jwt_required())
    @csrf_exempt
    def post(self, request, user_id):
        data = request.data

        # Create Role
        role_data = data.get('role')
        role_serializer = RoleSerializer(data=role_data)
        if role_serializer.is_valid():
            role = role_serializer.save()
        else:
            return Response(role_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Create Staff
        staff_data = {
            'gender': data.get('gender'),
            'tel': data.get('tel'),
            'email': data.get('email'),
            'birthday': data.get('birthday'),
            'hire_date': data.get('hire_date'),
            'role': role.id
        }
        staff_serializer = StaffSerializer(data=staff_data)
        if staff_serializer.is_valid():
            staff_serializer.save()
            return Response(staff_serializer.data, status=status.HTTP_201_CREATED)
        else:
            role.delete()
            return Response(staff_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StaffUpdateView(APIView):
    @method_decorator(jwt_required())
    @csrf_exempt
    def put(self, request, user_id, staff_id):
        try:
            staff = Staff.objects.get(id=staff_id)
        except Staff.DoesNotExist:
            return Response({'error': 'Staff not found'}, status=status.HTTP_404_NOT_FOUND)

        data = request.data

        # Update Role
        role_data = data.get('role')
        role_serializer = RoleSerializer(staff.role, data=role_data, partial=True)
        if role_serializer.is_valid():
            role_serializer.save()
        else:
            return Response(role_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Update Staff
        staff_data = {
            'gender': data.get('gender'),
            'tel': data.get('tel'),
            'email': data.get('email'),
            'birthday': data.get('birthday'),
            'hire_date': data.get('hire_date'),
            'role': staff.role.id
        }
        staff_serializer = StaffSerializer(staff, data=staff_data, partial=True)
        if staff_serializer.is_valid():
            staff_serializer.save()
            return Response(staff_serializer.data, status=status.HTTP_200_OK)
        return Response(staff_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class StaffDeleteView(APIView):
    @method_decorator(jwt_required())
    @csrf_exempt
    def delete(self, request, user_id, staff_id):
        try:
            staff = Staff.objects.get(id=staff_id)
        except Staff.DoesNotExist:
            return Response({'error': 'Staff not found'}, status=status.HTTP_404_NOT_FOUND)
        staff.delete()
        return Response({'message': 'Staff deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
