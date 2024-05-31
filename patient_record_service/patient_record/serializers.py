from rest_framework import serializers
from .models import InsuranceInformation, PatientRecord, VisitHistory


class InsuranceInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = InsuranceInformation
        fields = '__all__'


class VisitHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = VisitHistory
        fields = '__all__'


class PatientRecordSerializer(serializers.ModelSerializer):
    insurance_information = InsuranceInformationSerializer(read_only=True)
    visit_histories = VisitHistorySerializer(many=True, read_only=True)

    class Meta:
        model = PatientRecord
        fields = '__all__'
