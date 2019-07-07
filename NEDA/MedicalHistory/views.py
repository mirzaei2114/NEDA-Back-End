from django.shortcuts import render
from rest_framework import viewsets

from MedicalHistory.models import MedicalHistory
from MedicalHistory.serializers import MedicalHistorySerializer
from NEDA.permissions import IsSameDoctorIsDoctorOrReadonly


class MedicalHistoryViewSet(viewsets.ModelViewSet):
    permission_classes = (IsSameDoctorIsDoctorOrReadonly,)
    queryset = MedicalHistory.objects.all()
    serializer_class = MedicalHistorySerializer
