from rest_framework import serializers
from .models import Medicine, MedicineCategory, MedicineSupplier, Material, MaterialType, MaterialSupplier


class MedicineCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicineCategory
        fields = '__all__'


class MedicineSupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicineSupplier
        fields = '__all__'


class MedicineSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset=MedicineCategory.objects.all(), required=False)
    supplier = serializers.PrimaryKeyRelatedField(queryset=MedicineSupplier.objects.all(), required=False)

    class Meta:
        model = Medicine
        fields = '__all__'


class MaterialTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = MaterialType
        fields = '__all__'


class MaterialSupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = MaterialSupplier
        fields = '__all__'


class MaterialSerializer(serializers.ModelSerializer):
    type = serializers.PrimaryKeyRelatedField(queryset=MaterialType.objects.all(), required=False)
    supplier = serializers.PrimaryKeyRelatedField(queryset=MaterialSupplier.objects.all(), required=False)

    class Meta:
        model = Material
        fields = '__all__'
