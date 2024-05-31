from django.db import models

# Create your models here.
from django.db import models


class Appointment(models.Model):
    id = models.AutoField(primary_key=True)
    patient_id = models.IntegerField()
    hour = models.IntegerField()
    visit_date = models.DateField()
    note = models.TextField(blank=True, null=True)
    doctor_id = models.IntegerField()
    room_id = models.IntegerField()

    def __str__(self):
        return f"Appointment {self.id} on {self.visit_date} at {self.hour} for Patient {self.patient_id}"
