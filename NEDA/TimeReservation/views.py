from django.shortcuts import render
from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, mixins, filters, status
from rest_framework.response import Response

from Accounts.models import Patient, Doctor, Hospital
from NEDA.permissions import IsSameDoctorIsDoctorOrReadonly, ReserveTimePermission, TransactionPermission
from TimeReservation.models import Clinic, WorkingHour, AppointmentTime, Bonus, Transaction
from TimeReservation.serializers import ClinicSerializer, WorkingHourSerializer, \
    AppointmentTimeSerializer, BonusSerializer, TransactionSerializer


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

    def list(self, request, *args, **kwargs):
        if 'time_estimate' in request.query_params and request.query_params.get('time_estimate') == 'true':
            if request.user.is_authenticated and request.user.is_patient:
                patient = Patient.objects.get(user=request.user)
                patient_appointment_time = AppointmentTime.objects.filter(
                    patient=patient, date_time__date=timezone.now().date()).first()
                if patient_appointment_time:
                    if patient_appointment_time.clinic:
                        queryset = self.filter_queryset(
                            queryset=AppointmentTime.objects.filter(
                                clinic=patient_appointment_time.clinic,
                                date_time__date=timezone.now().date()).order_by('date_time'))
                    elif patient_appointment_time.hospital:
                        queryset = self.filter_queryset(
                            queryset=AppointmentTime.objects.filter(
                                hospital=patient_appointment_time.hospital,
                                date_time__date=timezone.now().date()).order_by('date_time'))
                else:
                    return Response({'Info': 'You have no appointment time today'}, status.HTTP_204_NO_CONTENT)
            elif request.user.is_authenticated and request.user.is_doctor:
                doctor = Doctor.objects.get(user=request.user)
                doctor_appointment_time = AppointmentTime.objects.filter(
                    doctor=doctor, date_time__date=timezone.now().date()).first()
                if doctor_appointment_time:
                    if doctor_appointment_time.clinic:
                        queryset = self.filter_queryset(
                            queryset=AppointmentTime.objects.filter(
                                clinic=doctor_appointment_time.clinic,
                                date_time__date=timezone.now().date()).order_by('date_time'))
                    elif doctor_appointment_time.hospital:
                        queryset = self.filter_queryset(
                            queryset=AppointmentTime.objects.filter(
                                hospital=doctor_appointment_time.hospital,
                                date_time__date=timezone.now().date()).order_by('date_time'))
                else:
                    return Response({'Info': 'You have no appointment time today'}, status.HTTP_204_NO_CONTENT)
            elif request.user.is_authenticated and request.user.is_hospital:
                hospital = Hospital.objects.get(user=request.user)
                hospital_appointment_time = AppointmentTime.objects.filter(
                    hospital=hospital, date_time__date=timezone.now().date()).first()
                if hospital_appointment_time:
                    queryset = self.filter_queryset(
                        queryset=AppointmentTime.objects.filter(
                            hospital=hospital_appointment_time.hospital,
                            date_time__date=timezone.now().date()).order_by('date_time'))
                else:
                    return Response({'Info': 'You have no appointment time today'}, status.HTTP_204_NO_CONTENT)
        else:
            queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class BonusViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = Bonus.objects.all()
    serializer_class = BonusSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('doctor', 'patient')


class TransactionViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.UpdateModelMixin,
                         viewsets.GenericViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    permission_classes = (TransactionPermission,)
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('appointment_time',)
