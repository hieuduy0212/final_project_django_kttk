from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import FullName, Address, RelativeInfo, Patient
from .serializers import FullNameSerializer, AddressSerializer, RelativeInfoSerializer, PatientSerializer
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


class PatientListView(APIView):
    @method_decorator(jwt_required())
    def get(self, request, user_id):
        patients = Patient.objects.all()
        serializer = PatientSerializer(patients, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PatientDetailView(APIView):
    @method_decorator(jwt_required())
    def get(self, request, user_id, patient_id):
        try:
            patient = Patient.objects.get(id=patient_id)
        except Patient.DoesNotExist:
            return Response({'error': 'Patient not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = PatientSerializer(patient)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PatientCreateView(APIView):
    @method_decorator(jwt_required())
    @csrf_exempt
    def post(self, request, user_id):
        data = request.data

        # Fetch patient record ID from another service
        token = request.headers.get('Authorization').split()[1]
        patient_record_url = f'http://localhost:8003/patient_records/{data.get("patient_id")}/'
        patient_record_data = fetch_data_from_service(patient_record_url, token)
        if not patient_record_data:
            return Response({'error': 'Patient record not found'}, status=status.HTTP_404_NOT_FOUND)

        # Create FullName
        full_name_data = data.get('full_name')
        full_name_serializer = FullNameSerializer(data=full_name_data)
        if full_name_serializer.is_valid():
            full_name = full_name_serializer.save()
        else:
            return Response(full_name_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Create Address
        address_data = data.get('address')
        address_serializer = AddressSerializer(data=address_data)
        if address_serializer.is_valid():
            address = address_serializer.save()
        else:
            full_name.delete()
            return Response(address_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Create RelativeInfo
        relative_info_data = data.get('relative_info')
        relative_info_serializer = RelativeInfoSerializer(data=relative_info_data)
        if relative_info_serializer.is_valid():
            relative_info = relative_info_serializer.save()
        else:
            full_name.delete()
            address.delete()
            return Response(relative_info_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Create Patient
        patient_data = {
            'patient_record_id': patient_record_data.get('id'),
            'tel': data.get('tel'),
            'relative_info': relative_info.id,
            'address': address.id,
            'full_name': full_name.id
        }
        patient_serializer = PatientSerializer(data=patient_data)
        if patient_serializer.is_valid():
            patient_serializer.save()
            return Response(patient_serializer.data, status=status.HTTP_201_CREATED)
        else:
            full_name.delete()
            address.delete()
            relative_info.delete()
            return Response(patient_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PatientUpdateView(APIView):
    @method_decorator(jwt_required())
    @csrf_exempt
    def put(self, request, user_id, patient_id):
        try:
            patient = Patient.objects.get(id=patient_id)
        except Patient.DoesNotExist:
            return Response({'error': 'Patient not found'}, status=status.HTTP_404_NOT_FOUND)

        data = request.data

        # Fetch patient record ID from another service
        token = request.headers.get('Authorization').split()[1]
        patient_record_url = f'http://localhost:8003/patient_records/{data.get("patient_id")}/'
        patient_record_data = fetch_data_from_service(patient_record_url, token)
        if not patient_record_data:
            return Response({'error': 'Patient record not found'}, status=status.HTTP_404_NOT_FOUND)

        # Update FullName
        full_name_data = data.get('full_name')
        full_name_serializer = FullNameSerializer(patient.full_name, data=full_name_data, partial=True)
        if full_name_serializer.is_valid():
            full_name_serializer.save()
        else:
            return Response(full_name_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Update Address
        address_data = data.get('address')
        address_serializer = AddressSerializer(patient.address, data=address_data, partial=True)
        if address_serializer.is_valid():
            address_serializer.save()
        else:
            return Response(address_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Update RelativeInfo
        relative_info_data = data.get('relative_info')
        relative_info_serializer = RelativeInfoSerializer(patient.relative_info, data=relative_info_data, partial=True)
        if relative_info_serializer.is_valid():
            relative_info_serializer.save()
        else:
            return Response(relative_info_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Update Patient
        patient_data = {
            'patient_record_id': patient_record_data.get('id'),
            'tel': data.get('tel'),
            'relative_info': patient.relative_info.id,
            'address': patient.address.id,
            'full_name': patient.full_name.id
        }
        patient_serializer = PatientSerializer(patient, data=patient_data, partial=True)
        if patient_serializer.is_valid():
            patient_serializer.save()
            return Response(patient_serializer.data, status=status.HTTP_200_OK)
        return Response(patient_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PatientDeleteView(APIView):
    @method_decorator(jwt_required())
    @csrf_exempt
    def delete(self, request, user_id, patient_id):
        try:
            patient = Patient.objects.get(id=patient_id)
        except Patient.DoesNotExist:
            return Response({'error': 'Patient not found'}, status=status.HTTP_404_NOT_FOUND)
        patient.delete()
        return Response({'message': 'Patient deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
