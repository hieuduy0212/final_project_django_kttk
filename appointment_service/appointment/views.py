from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Appointment
from .serializers import AppointmentSerializer
import requests
import jwt
from django.conf import settings
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt


# Utility function to fetch data from another service
def fetch_data_from_service(url):
    headers = {

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


class AppointmentListView(APIView):
    # @method_decorator(jwt_required())
    def get(self, request):
        appointments = Appointment.objects.all()
        serializer = AppointmentSerializer(appointments, many=True)
        appointments_data = []
        for appointment in serializer.data:
            doctor_url = f"http://localhost:8001/doctor/api/doctors/{appointment['doctor_id']}/"
            doctor_data = fetch_data_from_service(doctor_url)
            if not doctor_data:
                return Response({'error': 'Doctor not found'}, status=status.HTTP_404_NOT_FOUND)

            patient_url = f"http://localhost:8002/patients/api/patients/{appointment['patient_id']}/"
            patient_data = fetch_data_from_service(patient_url)
            if not patient_data:
                return Response({'error': 'Patient not found'}, status=status.HTTP_404_NOT_FOUND)

            response_data = appointment
            response_data['doctor'] = doctor_data
            response_data['patient'] = patient_data
            appointments_data.append(response_data)

        return Response(appointments_data, status=status.HTTP_200_OK)


class AppointmentDetailView(APIView):
    # @method_decorator(jwt_required())
    def get(self, request, appointment_id):
        try:
            appointment = Appointment.objects.get(id=appointment_id)

        except Appointment.DoesNotExist:
            return Response({'error': 'Appointment not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = AppointmentSerializer(appointment)
        doctor_url = f'http://localhost:8002/doctor/api/doctors/{appointment.doctor_id}/'
        doctor_data = fetch_data_from_service(doctor_url)
        if not doctor_data:
            return Response({'error': 'Doctor not found'}, status=status.HTTP_404_NOT_FOUND)

        patient_url = f'http://localhost:8003/patients/api/patients/{appointment.patient_id}/'
        patient_data = fetch_data_from_service(patient_url)
        if not patient_data:
            return Response({'error': 'Patient not found'}, status=status.HTTP_404_NOT_FOUND)
        response_data = serializer.data
        response_data['doctor'] = doctor_data
        response_data['patient'] = patient_data
        return Response(response_data, status=status.HTTP_200_OK)


class AppointmentCreateView(APIView):
    # @method_decorator(jwt_required())
    # @csrf_exempt
    def post(self, request):
        data = request.data
        doctor_id = data.get('doctor_id')
        patient_id = data.get('patient_id')
        # token = request.headers.get('Authorization').split()[1]

        # Fetch doctor details
        # doctor_url = f'http://localhost:8001/doctors/{doctor_id}/'
        # doctor_data = fetch_data_from_service(doctor_url, token)
        # if not doctor_data:
        #     return Response({'error': 'Doctor not found'}, status=status.HTTP_404_NOT_FOUND)

        # Fetch patient details
        # patient_url = f'http://localhost:8002/patients/{patient_id}/'
        # patient_data = fetch_data_from_service(patient_url, token)
        # if not patient_data:
        #     return Response({'error': 'Patient not found'}, status=status.HTTP_404_NOT_FOUND)

        print(doctor_data)
        print(patient_data)
        response_data = serializer.data
        response_data['doctor'] = doctor_data
        response_data['patient'] = patient_data
        return Response(response_data, status=status.HTTP_200_OK)


class AppointmentCreateView(APIView):
    # @method_decorator(jwt_required())
    # @csrf_exempt
    def post(self, request):
        data = request.data
        doctor_id = data.get('doctor_id')
        patient_id = data.get('patient_id')
        # token = request.headers.get('Authorization').split()[1]

        # Fetch doctor details
        # doctor_url = f'http://localhost:8001/doctors/{doctor_id}/'
        # doctor_data = fetch_data_from_service(doctor_url, token)
        # if not doctor_data:
        #     return Response({'error': 'Doctor not found'}, status=status.HTTP_404_NOT_FOUND)

        # Fetch patient details
        # patient_url = f'http://localhost:8002/patients/{patient_id}/'
        # patient_data = fetch_data_from_service(patient_url, token)
        # if not patient_data:
        #     return Response({'error': 'Patient not found'}, status=status.HTTP_404_NOT_FOUND)

        # Create appointment
        appointment_data = {
            'doctor_id': doctor_id,
            'patient_id': patient_id,
            'appointment_date': data.get('appointment_date'),
            'reason': data.get('reason'),
            'hour': data.get('hour'),
            'visit_date': data.get('visit_date'),
            'room_id': data.get('room_id')
        }
        serializer = AppointmentSerializer(data=appointment_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AppointmentUpdateView(APIView):
    # @method_decorator(jwt_required())
    # @csrf_exempt
    def put(self, request, appointment_id):
        try:
            appointment = Appointment.objects.get(id=appointment_id)
        except Appointment.DoesNotExist:
            return Response({'error': 'Appointment not found'}, status=status.HTTP_404_NOT_FOUND)

        data = request.data
        doctor_id = data.get('doctor_id')
        patient_id = data.get('patient_id')
        # token = request.headers.get('Authorization').split()[1]

        # Fetch doctor details
        # doctor_url = f'http://localhost:8001/doctors/{doctor_id}/'
        # doctor_data = fetch_data_from_service(doctor_url, token)
        # if not doctor_data:
        #     return Response({'error': 'Doctor not found'}, status=status.HTTP_404_NOT_FOUND)

        # Fetch patient details
        # patient_url = f'http://localhost:8002/patients/{patient_id}/'
        # patient_data = fetch_data_from_service(patient_url, token)
        # if not patient_data:
        #     return Response({'error': 'Patient not found'}, status=status.HTTP_404_NOT_FOUND)

        # Update appointment
        appointment_data = {
            'doctor_id': doctor_id,
            'patient_id': patient_id,
            'appointment_date': data.get('appointment_date'),
            'reason': data.get('reason')
        }
        serializer = AppointmentSerializer(appointment, data=appointment_data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AppointmentDeleteView(APIView):
    # @method_decorator(jwt_required())
    # @csrf_exempt
    def delete(self, request, appointment_id):
        try:
            appointment = Appointment.objects.get(id=appointment_id)
        except Appointment.DoesNotExist:
            return Response({'error': 'Appointment not found'}, status=status.HTTP_404_NOT_FOUND)
        appointment.delete()
        return Response({'message': 'Appointment deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
