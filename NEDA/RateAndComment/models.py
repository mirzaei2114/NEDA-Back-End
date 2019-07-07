from django.db import models

# Create your models here.
from Accounts.models import Patient, Doctor, Hospital
from TimeReservation.models import Clinic


class DoctorRate(models.Model):
    id = models.AutoField(primary_key=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='patient_doctor_rates')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='doctor_rates')
    rate = models.FloatField()

    def __str__(self):
        return self.id


class DoctorComment(models.Model):
    id = models.AutoField(primary_key=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='patient_doctor_comments')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='doctor_comments')
    comment = models.CharField(max_length=512)

    def __str__(self):
        return self.id


class HospitalRate(models.Model):
    id = models.AutoField(primary_key=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='patient_hospital_rates')
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE, related_name='hospital_rates')
    rate = models.FloatField()

    def __str__(self):
        return self.id


class HospitalComment(models.Model):
    id = models.AutoField(primary_key=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='patient_hospital_comments')
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE, related_name='hospital_comments')
    comment = models.CharField(max_length=512)

    def __str__(self):
        return self.id


class ClinicRate(models.Model):
    id = models.AutoField(primary_key=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='patient_clinic_rates')
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE, related_name='clinic_rates')
    rate = models.FloatField()

    def __str__(self):
        return self.id


class ClinicComment(models.Model):
    id = models.AutoField(primary_key=True)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='patient_clinic_comments')
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE, related_name='clinic_comments')
    comment = models.CharField(max_length=512)

    def __str__(self):
        return self.id
