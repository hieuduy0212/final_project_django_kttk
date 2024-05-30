from rest_framework import serializers
from .models import Specialist, Address, Department, FullName, Doctor

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'

class SpecialistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Specialist
        fields = '__all__'

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'

class FullNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = FullName
        fields = '__all__'

class DoctorSerializer(serializers.ModelSerializer):
    specialist = serializers.PrimaryKeyRelatedField(queryset=Specialist.objects.all(), required=False)
    address = AddressSerializer(required=False)
    full_name = FullNameSerializer(required=False)
    department = serializers.PrimaryKeyRelatedField(queryset=Department.objects.all(), required=False)

    class Meta:
        model = Doctor
        fields = '__all__'

    def create(self, validated_data):
        address_data = validated_data.pop('address')
        full_name_data = validated_data.pop('full_name')

        address_instance = Address.objects.create(**address_data)
        full_name_instance = FullName.objects.create(**full_name_data)

        validated_data['address'] = address_instance
        validated_data['full_name'] = full_name_instance

        return Doctor.objects.create(**validated_data)
