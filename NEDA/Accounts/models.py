from django import forms
from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager as Django_UserManager
# Create your models here.
from django.utils import timezone
from rest_framework.authtoken.models import Token


__PROVINCES = ['آذربایجان شرقی', 'آذربایجان غربی', 'اردبیل', 'اردبیل', 'اصفهان', 'البرز', 'ایلام', 'بوشهر', 'تهران',
               'چهارمحال و بختیاری', 'خراسان جنوبی', 'خراسان رضوی', 'خراسان شمالی', 'خوزستان', 'زنجان', 'سمنان',
               'سیستان و بلوچستان', 'فارس', 'قزوین', 'قم', 'کردستان', 'کرمان', 'کرمانشاه', 'کهگیلویه و بویراحمد',
               'گلستان', 'گیلان', 'لرستان', 'مازندران', 'مرکزی', 'هرمزگان', 'همدان', 'یزد']
PROVINCES_CHOICES = [(item, item) for item in __PROVINCES]

__GENDERS = ['زن', 'مرد']
GENDERS_CHOICES = [(item, item) for item in __GENDERS]


class MyUser(AbstractUser):
    province = models.CharField(choices=PROVINCES_CHOICES, max_length=19, blank=True)
    is_doctor = models.BooleanField(default=False)
    is_patient = models.BooleanField(default=False)
    is_hospital = models.BooleanField(default=False)

    def __str__(self):
        return self.username


class Patient(models.Model):
    user = models.OneToOneField(MyUser, on_delete=models.CASCADE, related_name='patient_user')
    social_number = models.CharField(max_length=10, primary_key=True)
    gender = models.CharField(choices=GENDERS_CHOICES, max_length=3)
    phone_number = models.CharField(max_length=8, blank=True)
    mobile_number = models.CharField(help_text='Like 09XXXXXXXXX', max_length=11, unique=True)
    address = models.CharField(max_length=512, blank=True)
    date_of_birth = models.DateField(null=True)
    picture = models.ImageField(upload_to='Profile Pictures/Patients/', default='Profile Pictures/Patients/default.png',
                                blank=True)
    wallet = models.FloatField(default=0)

    def __str__(self):
        return self.social_number


class Doctor(models.Model):
    user = models.OneToOneField(MyUser, on_delete=models.CASCADE, related_name='doctor_user')
    medical_system_number = models.CharField(primary_key=True, max_length=50)
    gender = models.CharField(choices=GENDERS_CHOICES, max_length=3)
    date_of_birth = models.DateField(null=True)
    expertise = models.CharField(max_length=50)
    mobile_number = models.CharField(help_text='Like 09XXXXXXXXX', max_length=11, unique=True)
    bio = models.CharField(max_length=1024, default='درباره شما :)')
    picture = models.ImageField(upload_to='Profile Pictures/Doctors/', default='Profile Pictures/Doctors/default.png',
                                blank=True)

    def __str__(self):
        return self.medical_system_number


class Hospital(models.Model):
    user = models.OneToOneField(MyUser, on_delete=models.CASCADE, related_name='hospital_user')
    phone_number = models.CharField(max_length=8)
    address = models.CharField(max_length=512)
    post_code = models.CharField(max_length=10, primary_key=True)
    doctors = models.ManyToManyField(Doctor, null=True, related_name='hospitals')
    bio = models.TextField(default='درباره بیمارستان :)')
    picture = models.ImageField(upload_to='Profile Pictures/Hospitals/',
                                default='Profile Pictures/Hospitals/default.png', blank=True)

    def __str__(self):
        return self.post_code


class UserManager(Django_UserManager):

    def create_superuser(self, username, email, password, **extra_fields):
        """
        Creates and saves a User with the given username, email and password.
        """
        now = timezone.now()
        if not username:
            raise ValueError('The given username must be set')
        email = UserManager.normalize_email(email)
        user = MyUser(username=username, email=email,
                      is_staff=True, is_active=True, is_superuser=True,
                      last_login=now, date_joined=now)

        user.set_password(password)
        user.save(using=self._db)


