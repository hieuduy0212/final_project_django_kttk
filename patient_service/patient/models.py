from django.db import models


class FullName(models.Model):
    first_name = models.CharField(max_length=255)
    mid_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.first_name} {self.mid_name} {self.last_name}" if self.mid_name else f"{self.first_name} {self.last_name}"


class Address(models.Model):
    no_house = models.IntegerField()
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.noHouse}, {self.street}, {self.city}"


class RelativeInfo(models.Model):
    full_name = models.CharField(max_length=255)
    tel = models.CharField(max_length=15)
    address = models.CharField(max_length=255)

    def __str__(self):
        return self.full_name


class Patient(models.Model):
    tel = models.CharField(max_length=15)
    relative_info = models.ForeignKey(RelativeInfo, on_delete=models.CASCADE)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    full_name = models.ForeignKey(FullName, on_delete=models.CASCADE)

    def __str__(self):
        return f"Patient {self.full_name}"
