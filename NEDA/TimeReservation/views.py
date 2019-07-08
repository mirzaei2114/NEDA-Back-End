from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, mixins, filters

from NEDA.permissions import IsSameDoctorIsDoctorOrReadonly, ReserveTimePermission
from TimeReservation.models import Clinic, WorkingHour, AppointmentTime, Bonus
from TimeReservation.serializers import ClinicSerializer, WorkingHourSerializer, \
    AppointmentTimeSerializer, BonusSerializer


# Create your views here.


class ClinicViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    permission_classes = (IsSameDoctorIsDoctorOrReadonly,)
    queryset = Clinic.objects.all()
    serializer_class = ClinicSerializer
    filter_backends = (filters.SearchFilter, DjangoFilterBackend,)
    search_fields = ('name', 'address')
    filterset_fields = ('province', 'doctor')


class WorkingHourViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    permission_classes = (IsSameDoctorIsDoctorOrReadonly,)
    queryset = WorkingHour.objects.all()
    serializer_class = WorkingHourSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('day', 'doctor', 'clinic', 'hospital')


class AppointmentTimeViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin,
                             mixins.UpdateModelMixin, viewsets.GenericViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    permission_classes = (ReserveTimePermission,)
    queryset = AppointmentTime.objects.all()
    serializer_class = AppointmentTimeSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('date_time', 'doctor', 'patient', 'clinic', 'hospital')


class BonusViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = Bonus.objects.all()
    serializer_class = BonusSerializer
