from django.shortcuts import render
from rest_framework import viewsets, mixins

from NEDA.permissions import IsSameDoctorIsDoctorOrReadonly, ReserveTimePermission
from TimeReservation.models import Clinic, WorkingHour, AppointmentTime
from TimeReservation.serializers import ClinicSerializer, WorkingHourSerializer,\
    AppointmentTimeSerializer


# Create your views here.


class ClinicViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    permission_classes = (IsSameDoctorIsDoctorOrReadonly,)
    queryset = Clinic.objects.all()
    serializer_class = ClinicSerializer


class WorkingHourViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    permission_classes = (IsSameDoctorIsDoctorOrReadonly,)
    queryset = WorkingHour.objects.all()
    serializer_class = WorkingHourSerializer


class AppointmentTimeViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin,
                             mixins.UpdateModelMixin, viewsets.GenericViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    permission_classes = (ReserveTimePermission,)
    queryset = AppointmentTime.objects.all()
    serializer_class = AppointmentTimeSerializer
