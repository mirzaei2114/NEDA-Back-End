"""NEDA URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token

from Accounts.views import PatientViewSet, DoctorViewSet, HospitalViewSet, UserViewSet
from MedicalHistory.views import MedicalHistoryViewSet
from TimeReservation.views import ClinicViewSet, AppointmentTimeViewSet, WorkingHourViewSet
from RateAndComment.views import DoctorRateViewSet, DoctorCommentViewSet, ClinicCommentViewSet, ClinicRateViewSet, \
    HospitalCommentViewSet, HospitalRateViewSet

from django.conf.urls.static import static
from NEDA import settings

router = routers.DefaultRouter()
router.register('users', UserViewSet)
router.register('patients', PatientViewSet)
router.register('doctors', DoctorViewSet)
router.register('hospitals', HospitalViewSet)
router.register('clinics', ClinicViewSet)
router.register('working_hours', WorkingHourViewSet)
router.register('appointment_times', AppointmentTimeViewSet)
router.register('medical_histories', MedicalHistoryViewSet)
router.register('doctor_rates', DoctorRateViewSet)
router.register('doctor_comments', DoctorCommentViewSet)
router.register('hospital_rates', HospitalRateViewSet)
router.register('hospital_comments', HospitalCommentViewSet)
router.register('clinic_rates', ClinicRateViewSet)
router.register('clinic_comments', ClinicCommentViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', include('rest_framework.urls')),
    url(r'^get_token/', obtain_auth_token),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
