from django.db import models


class Specialist(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True)


class Address(models.Model):
    no_house = models.CharField(max_length=50)
    street = models.CharField(max_length=100)
    city = models.CharField(max_length=100)


class Department(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True)


class FullName(models.Model):
    first_name = models.CharField(max_length=50)
    mid_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50)


class Doctor(models.Model):
    gender = models.CharField(max_length=10)
    tel = models.CharField(max_length=20)
    email = models.EmailField()
    specialist = models.ForeignKey(Specialist, on_delete=models.CASCADE)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    full_name = models.ForeignKey(FullName, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
