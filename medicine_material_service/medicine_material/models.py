from django.db import models


class MedicineCategory(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name


class MedicineSupplier(models.Model):
    name = models.CharField(max_length=255)
    tel = models.CharField(max_length=15)
    email = models.EmailField()
    address = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Medicine(models.Model):
    name = models.CharField(max_length=255)
    brand = models.CharField(max_length=255)
    category = models.ForeignKey(MedicineCategory, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    supplier = models.ForeignKey(MedicineSupplier, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class MaterialType(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name


class MaterialSupplier(models.Model):
    name = models.CharField(max_length=255)
    tel = models.CharField(max_length=15)
    email = models.EmailField()
    address = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Material(models.Model):
    name = models.CharField(max_length=255)
    type = models.ForeignKey(MaterialType, related_name='materials', on_delete=models.CASCADE)
    quantity = models.IntegerField()
    supplier = models.ForeignKey(MaterialSupplier, related_name='materials', on_delete=models.CASCADE)

    def __str__(self):
        return self.name
