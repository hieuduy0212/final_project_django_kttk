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
    category = MedicineCategorySerializer(read_only=True)
    supplier = MedicineSupplierSerializer(read_only=True)

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
    type = MaterialTypeSerializer(read_only=True)
    supplier = MaterialSupplierSerializer(read_only=True)

    class Meta:
        model = Material
        fields = '__all__'
