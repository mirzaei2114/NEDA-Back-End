from django.db import models

from Accounts.models import Patient, Doctor


class MedicalHistory(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.DateField()
    content = models.CharField(max_length=512)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='patient_medical_histories')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='doctor_medical_histories')
    # doctors never remove!
