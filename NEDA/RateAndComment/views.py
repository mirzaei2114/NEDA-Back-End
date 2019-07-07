from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets

from RateAndComment.models import DoctorRate, DoctorComment, HospitalRate, HospitalComment, ClinicRate, ClinicComment
from RateAndComment.serializers import DoctorRateSerializer, DoctorCommentSerializer, HospitalRateSerializer, \
    HospitalCommentSerializer, ClinicRateSerializer, ClinicCommentSerializer
from NEDA.permissions import IsSamePatientAuthenticatedOrReadOnly


class DoctorRateViewSet(viewsets.ModelViewSet):
    permission_classes = (IsSamePatientAuthenticatedOrReadOnly,)
    queryset = DoctorRate.objects.all()
    serializer_class = DoctorRateSerializer


class DoctorCommentViewSet(viewsets.ModelViewSet):
    permission_classes = (IsSamePatientAuthenticatedOrReadOnly,)
    queryset = DoctorComment.objects.all()
    serializer_class = DoctorCommentSerializer


class HospitalRateViewSet(viewsets.ModelViewSet):
    permission_classes = (IsSamePatientAuthenticatedOrReadOnly,)
    queryset = HospitalRate.objects.all()
    serializer_class = HospitalRateSerializer


class HospitalCommentViewSet(viewsets.ModelViewSet):
    permission_classes = (IsSamePatientAuthenticatedOrReadOnly,)
    queryset = HospitalComment.objects.all()
    serializer_class = HospitalCommentSerializer


class ClinicRateViewSet(viewsets.ModelViewSet):
    permission_classes = (IsSamePatientAuthenticatedOrReadOnly,)
    queryset = ClinicRate.objects.all()
    serializer_class = ClinicRateSerializer


class ClinicCommentViewSet(viewsets.ModelViewSet):
    permission_classes = (IsSamePatientAuthenticatedOrReadOnly,)
    queryset = ClinicComment.objects.all()
    serializer_class = ClinicCommentSerializer
