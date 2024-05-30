from django.contrib.auth.models import AbstractUser
from django.db import models

class Address(models.Model):
  houseNumber = models.CharField(max_length=255)
  street = models.CharField(max_length=255)
  city = models.CharField(max_length=255)
  district = models.CharField(max_length=255)
  nationality = models.CharField(max_length=255)

  def __str__(self):
    return f"{self.houseNumber}, {self.street}, {self.city}, {self.district}, {self.nationality}"

class FullName(models.Model):
  first_name = models.CharField(max_length=255)
  last_name = models.CharField(max_length=255)
  mid_name = models.CharField(max_length=255, blank=True, null=True)

  def __str__(self):
    return f"{self.first_name} {self.mid_name} {self.last_name}" if self.mid_name else f"{self.first_name} {self.last_name}"

class User(AbstractUser):
  email = models.CharField(max_length=255, unique=True)
  password = models.CharField(max_length=255)
  username = None
  full_name = models.ForeignKey(FullName, on_delete=models.CASCADE, null=True, blank=True)
  address = models.ForeignKey(Address, on_delete=models.CASCADE, null=True, blank=True)

  USERNAME_FIELD = 'email'
  REQUIRED_FIELDS = []

  def __str__(self):
    return self.email
