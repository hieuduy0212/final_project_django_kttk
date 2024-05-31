from rest_framework import serializers
from .models import Invoice, Payment, InvoiceMedicine


class InvoiceMedicineSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvoiceMedicine
        fields = '__all__'


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'


class InvoiceSerializer(serializers.ModelSerializer):
    invoice_medicines = InvoiceMedicineSerializer(many=True, read_only=True)
    payment = PaymentSerializer(read_only=True)

    class Meta:
        model = Invoice
        fields = '__all__'
