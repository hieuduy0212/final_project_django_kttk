from rest_framework import serializers
from .models import FullName, Address, RelativeInfo, Patient


class FullNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = FullName
        fields = '__all__'


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'


class RelativeInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = RelativeInfo
        fields = '__all__'


class PatientSerializer(serializers.ModelSerializer):
    full_name = FullNameSerializer(read_only=True)
    address = AddressSerializer(read_only=True)
    relative_info = RelativeInfoSerializer(read_only=True)

    class Meta:
        model = Patient
        fields = '__all__'
