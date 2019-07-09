
from django.db import models

# Create your models here.
from Accounts.models import Doctor, Patient, Hospital, PROVINCES_CHOICES

DAYS_PER = ['شنبه', 'یکشنبه', 'دوشنبه', 'سه شنبه', 'چهارشنبه', 'پنج شنبه', 'جمعه']
DAYS_CHOICES = [(item, item) for item in DAYS_PER]


class Clinic(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=64)
    province = models.CharField(choices=PROVINCES_CHOICES, max_length=19)
    phone_number = models.CharField(max_length=8)
    address = models.CharField(max_length=512)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='doctor_clinics')
    rate = models.FloatField(default=2.5)
    rate_number = models.BigIntegerField(default=0)

    def __str__(self):
        return str(self.id)


class WorkingHour(models.Model):
    id = models.AutoField(primary_key=True)
    day = models.CharField(choices=DAYS_CHOICES, max_length=8)
    start = models.TimeField()
    end = models.TimeField()
    period = models.IntegerField(help_text='in minutes')
    price = models.IntegerField()
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='doctor_working_hours')
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE, null=True, related_name='clinic_working_hours')
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE, null=True, related_name='hospital_working_hours')

    def __str__(self):
        return self.id


class AppointmentTime(models.Model):
    id = models.AutoField(primary_key=True)
    date_time = models.DateTimeField()
    reservation_date_time = models.DateTimeField(null=True)
    has_reserved = models.BooleanField(default=False)
    has_paid = models.BooleanField(default=False)
    visitation_time = models.TimeField(null=True, default=None)
    visiting = models.BooleanField(default=False)
    visited = models.BooleanField(default=False)
    price = models.IntegerField()
    bonus_amount = models.FloatField(default=0)
    total_price = models.FloatField(default=0)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='doctor_appointment_times')
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, null=True, related_name='patient_appointment_times')
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE, null=True, related_name='clinic_appointment_times')
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE, null=True,
                                 related_name='hospital_appointment_times')

    def __str__(self):
        return str(self.id)


class Bonus(models.Model):
    id = models.AutoField(primary_key=True)
    amount = models.FloatField()
    doctor = models.OneToOneField(Doctor, on_delete=models.CASCADE)
    patient = models.OneToOneField(Patient, on_delete=models.CASCADE)

    def __str__(self):
        return self.id


class Transaction(models.Model):
    id = models.AutoField(primary_key=True)
    price = models.IntegerField()
    card_number = models.IntegerField(max_length=16, null=True)
    date_time = models.DateTimeField(null=True)
    success = models.BooleanField(default=False)
    appointment_time = models.OneToOneField(AppointmentTime, on_delete=models.CASCADE,
                                            related_name='appointment_time_transaction')

    def __str__(self):
        return str(self.id)
