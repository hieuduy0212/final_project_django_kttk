from django.db import models


class InsuranceInformation(models.Model):
    type = models.CharField(max_length=255)
    code = models.CharField(max_length=255)
    date_issue = models.DateField()
    expire_issue = models.DateField()

    def __str__(self):
        return f"Insurance {self.code} for Patient Record {self.patient_record_id}"


class PatientRecord(models.Model):
    patient_id = models.IntegerField()
    insurance_information = models.OneToOneField(InsuranceInformation, on_delete=models.SET_NULL, null=True, blank=True,
                                                 related_name='patient_record')
    visit_histories = models.ManyToManyField('VisitHistory', related_name='patient_records')

    def __str__(self):
        return f"Patient Record {self.id} for Patient {self.patient_id}"


class VisitHistory(models.Model):
    visit_date = models.DateField()
    reason = models.CharField(max_length=255)
    doctor_id = models.IntegerField()
    result = models.TextField()
    appointment_id = models.IntegerField()
    invoice_id = models.IntegerField()
    patient_record_id = models.IntegerField()

    def __str__(self):
        return f"Visit on {self.visit_date} for Patient Record {self.patient_record_id}"
