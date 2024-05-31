from rest_framework import serializers
from .models import FullName, Address, RelativeInfo, Patient

class FullNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = FullName
        fields = '__all__'

    def to_internal_value(self, data):
        if isinstance(data, int):
            return FullName.objects.get(pk=data)
        return super().to_internal_value(data)

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = '__all__'

    def to_internal_value(self, data):
        if isinstance(data, int):
            return Address.objects.get(pk=data)
        return super().to_internal_value(data)

class RelativeInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = RelativeInfo
        fields = '__all__'

    def to_internal_value(self, data):
        if isinstance(data, int):
            return RelativeInfo.objects.get(pk=data)
        return super().to_internal_value(data)

class PatientSerializer(serializers.ModelSerializer):
    full_name = FullNameSerializer(required=False)
    address = AddressSerializer(required=False)
    relative_info = RelativeInfoSerializer(required=False)

    class Meta:
        model = Patient
        fields = '__all__'
