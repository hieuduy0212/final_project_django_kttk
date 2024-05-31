from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Invoice, Payment, InvoiceMedicine
from .serializers import InvoiceSerializer, PaymentSerializer, InvoiceMedicineSerializer
import requests
import jwt
from django.conf import settings
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt


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


class InvoiceListView(APIView):
    @method_decorator(jwt_required())
    def get(self, request, user_id):
        invoices = Invoice.objects.all()
        serializer = InvoiceSerializer(invoices, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class InvoiceDetailView(APIView):
    @method_decorator(jwt_required())
    def get(self, request, user_id, invoice_id):
        try:
            invoice = Invoice.objects.get(id=invoice_id)
        except Invoice.DoesNotExist:
            return Response({'error': 'Invoice not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = InvoiceSerializer(invoice)
        return Response(serializer.data, status=status.HTTP_200_OK)


class InvoiceCreateView(APIView):
    @method_decorator(jwt_required())
    @csrf_exempt
    def post(self, request, user_id):
        data = request.data
        patient_id = data.get('patient_id')
        token = request.headers.get('Authorization').split()[1]

        # Fetch patient details
        patient_url = f'http://localhost:8002/patients/{patient_id}/'
        patient_data = fetch_data_from_service(patient_url, token)
        if not patient_data:
            return Response({'error': 'Patient not found'}, status=status.HTTP_404_NOT_FOUND)

        # Create invoice
        serializer = InvoiceSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class InvoiceUpdateView(APIView):
    @method_decorator(jwt_required())
    @csrf_exempt
    def put(self, request, user_id, invoice_id):
        try:
            invoice = Invoice.objects.get(id=invoice_id)
        except Invoice.DoesNotExist:
            return Response({'error': 'Invoice not found'}, status=status.HTTP_404_NOT_FOUND)

        data = request.data
        patient_id = data.get('patient_id')
        token = request.headers.get('Authorization').split()[1]

        # Fetch patient details
        patient_url = f'http://localhost:8002/patients/{patient_id}/'
        patient_data = fetch_data_from_service(patient_url, token)
        if not patient_data:
            return Response({'error': 'Patient not found'}, status=status.HTTP_404_NOT_FOUND)

        # Update invoice
        serializer = InvoiceSerializer(invoice, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class InvoiceDeleteView(APIView):
    @method_decorator(jwt_required())
    @csrf_exempt
    def delete(self, request, user_id, invoice_id):
        try:
            invoice = Invoice.objects.get(id=invoice_id)
        except Invoice.DoesNotExist:
            return Response({'error': 'Invoice not found'}, status=status.HTTP_404_NOT_FOUND)
        invoice.delete()
        return Response({'message': 'Invoice deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
