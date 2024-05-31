from django.db import models


class Invoice(models.Model):
    patient_id = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    payment = models.ForeignKey('Payment', related_name='invoices', on_delete=models.CASCADE)

    def __str__(self):
        return f"Invoice {self.id} for Patient {self.patient_id}"


class Payment(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name


class InvoiceMedicine(models.Model):
    invoice = models.ForeignKey(Invoice, related_name='invoice_medicines', on_delete=models.CASCADE)
    medicine_id = models.IntegerField()
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Medicine {self.medicine_id} in Invoice {self.invoice.id}"
