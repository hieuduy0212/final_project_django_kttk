from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import InsuranceInformation, PatientRecord, VisitHistory
from .serializers import InsuranceInformationSerializer, PatientRecordSerializer, VisitHistorySerializer


class PatientRecordCreateView(APIView):
    def post(self, request):
        data = request.data
        insurance_data = data.pop('insurance_information', None)
        visit_histories_data = data.pop('visit_histories', [])

        insurance = None
        if insurance_data:
            insurance_serializer = InsuranceInformationSerializer(data=insurance_data)
            if insurance_serializer.is_valid():
                insurance = insurance_serializer.save()
            else:
                return Response(insurance_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        patient_record_serializer = PatientRecordSerializer(data=data)
        if patient_record_serializer.is_valid():
            patient_record = patient_record_serializer.save(insurance_information=insurance)

            for visit_history_data in visit_histories_data:
                visit_history_serializer = VisitHistorySerializer(data=visit_history_data)
                if visit_history_serializer.is_valid():
                    visit_history_serializer.save(patient_record=patient_record)
                else:
                    return Response(visit_history_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            return Response(patient_record_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(patient_record_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PatientRecordUpdateView(APIView):
    def put(self, request, pk):
        try:
            patient_record = PatientRecord.objects.get(pk=pk)
        except PatientRecord.DoesNotExist:
            return Response({'error': 'PatientRecord not found'}, status=status.HTTP_404_NOT_FOUND)

        data = request.data
        insurance_data = data.pop('insurance_information', None)
        visit_histories_data = data.pop('visit_histories', [])

        if insurance_data:
            if patient_record.insurance_information:
                insurance_serializer = InsuranceInformationSerializer(patient_record.insurance_information, data=insurance_data)
            else:
                insurance_serializer = InsuranceInformationSerializer(data=insurance_data)

            if insurance_serializer.is_valid():
                insurance = insurance_serializer.save()
                patient_record.insurance_information = insurance
            else:
                return Response(insurance_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        patient_record_serializer = PatientRecordSerializer(patient_record, data=data)
        if patient_record_serializer.is_valid():
            patient_record = patient_record_serializer.save()

            for visit_history_data in visit_histories_data:
                visit_history_serializer = VisitHistorySerializer(data=visit_history_data)
                if visit_history_serializer.is_valid():
                    visit_history_serializer.save(patient_record=patient_record)
                else:
                    return Response(visit_history_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            return Response(patient_record_serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(patient_record_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VisitHistoryCreateView(APIView):
    def post(self, request):
        data = request.data
        visit_history_serializer = VisitHistorySerializer(data=data)
        if visit_history_serializer.is_valid():
            visit_history_serializer.save()
            return Response(visit_history_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(visit_history_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PatientRecordListView(APIView):
    def get(self, request):
        patient_records = PatientRecord.objects.all()
        serializer = PatientRecordSerializer(patient_records, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PatientRecordDetailView(APIView):
    def get(self, request, patient_id):
        try:
            patient_record = PatientRecord.objects.get(patient_id=patient_id)
        except PatientRecord.DoesNotExist:
            return Response({'error': 'PatientRecord not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = PatientRecordSerializer(patient_record)
        return Response(serializer.data, status=status.HTTP_200_OK)


class VisitHistoryListView(APIView):
    def get(self, request, patient_record_id):
        visit_histories = VisitHistory.objects.filter(patient_record_id=patient_record_id)
        serializer = VisitHistorySerializer(visit_histories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
