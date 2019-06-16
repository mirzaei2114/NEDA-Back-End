from django.utils import timezone
from datetime import timedelta, datetime

from rest_framework import serializers
from Accounts.models import Doctor, Patient, Hospital
from TimeReservation.models import Clinic, WorkingHour, AppointmentTime, DAYS_PER


class ClinicSerializer(serializers.HyperlinkedModelSerializer):
    doctor = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Clinic
        fields = ('url', 'id', 'name', 'phone_number', 'address', 'doctor')

    def create(self, validated_data):
        try:
            doctor = None
            request = self.context.get("request")
            if request and hasattr(request, "user"):
                user = request.user
                doctor = Doctor.objects.get(user=user)
            validated_data['doctor'] = doctor
            instance = Clinic.objects.create(**validated_data)
            instance.save()
            return instance
        except Exception as e:
            raise serializers.ValidationError('Bad Request at: ' + str(e.args))


class WorkingHourSerializer(serializers.HyperlinkedModelSerializer):
    doctor = serializers.PrimaryKeyRelatedField(read_only=True)
    clinic = serializers.PrimaryKeyRelatedField(many=False, queryset=Clinic.objects.all(), allow_null=True)
    hospital = serializers.PrimaryKeyRelatedField(many=False, queryset=Hospital.objects.all(), allow_null=True)

    class Meta:
        model = WorkingHour
        fields = ('url', 'id', 'day', 'start', 'end', 'period', 'price', 'doctor', 'clinic', 'hospital')

    def validate(self, attrs):
        print(attrs)
        if [attrs['clinic'], attrs['hospital']].count(None) != 1:
            raise serializers.ValidationError('Both clinic and hospital can not be null')

        doctor = None
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            user = request.user
            doctor = Doctor.objects.get(user=user)
        if attrs['clinic']:
            if attrs['clinic'].doctor != doctor:
                raise serializers.ValidationError('You can choose only your clinic')
        elif attrs['hospital']:
            if doctor not in list(attrs['hospital'].doctors.all()):
                raise serializers.ValidationError('You can choose only your hospital')

        if attrs['period'] <= 0:
            raise serializers.ValidationError('Period must be greater than zero')

        now = datetime.now()
        start = datetime(now.year, now.month, now.day,
                         attrs['start'].hour, attrs['start'].minute)
        end = datetime(now.year, now.month, now.day,
                       attrs['end'].hour, attrs['end'].minute)
        if start + timedelta(minutes=attrs['period']) > end:
            raise serializers.ValidationError('We should be able to create at least'
                                              ' one appointment time between start and end')
        return super().validate(attrs)

    def create(self, validated_data):
        instance = None
        try:
            doctor = None
            request = self.context.get("request")
            if request and hasattr(request, "user"):
                user = request.user
                doctor = Doctor.objects.get(user=user)
            validated_data['doctor'] = doctor
            instance = WorkingHour.objects.create(**validated_data)
            instance.save()
        except Exception as e:
            raise serializers.ValidationError('Bad Request at: ' + str(e.args))
        appointments = []
        try:
            now = datetime.now()
            current_day = now.weekday() + 2
            difference_from_tomorrow = (DAYS_PER.index(instance.day) - current_day + 6) % 7
            start = datetime(now.year, now.month, now.day,
                             instance.start.hour, instance.start.minute) + timedelta(days=difference_from_tomorrow + 1)
            end = datetime(now.year, now.month, now.day,
                           instance.end.hour, instance.end.minute) + timedelta(days=difference_from_tomorrow + 1)
            period = instance.period
            for i in range(2):
                appointment_datetime = start
                while appointment_datetime + timedelta(minutes=period) <= end:
                    data = {'date_time': appointment_datetime, 'reservation_date_time': None, 'has_reserved': False,
                            'price': instance.price, 'doctor': doctor, 'patient': None, 'clinic': instance.clinic,
                            'hospital': instance.hospital}
                    appointment_time = AppointmentTime.objects.create(**data)
                    appointments.append(appointment_time)
                    appointment_datetime += timedelta(minutes=period)
                    appointment_time.save()
                start += timedelta(days=7)
                end += timedelta(days=7)
            return instance
        except Exception as e:
            if instance:
                instance.delete()
            for appointment in appointments:
                if appointment:
                    appointment.delete()
            raise serializers.ValidationError('Bad Request at: ' + str(e.args))


class AppointmentTimeSerializer(serializers.HyperlinkedModelSerializer):
    doctor = serializers.PrimaryKeyRelatedField(read_only=True)
    patient = serializers.PrimaryKeyRelatedField(read_only=True)
    reservation_date_time = serializers.DateTimeField(read_only=True)
    clinic = serializers.PrimaryKeyRelatedField(read_only=True)
    hospital = serializers.PrimaryKeyRelatedField(read_only=True)
    price = serializers.PrimaryKeyRelatedField(read_only=True)
    date_time = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = AppointmentTime
        fields = ('url', 'id', 'date_time', 'reservation_date_time', 'has_reserved', 'price',
                  'doctor', 'patient', 'clinic', 'hospital')

    def update(self, instance, validated_data):
        try:
            if not instance.has_reserved and validated_data['has_reserved']:
                patient = None
                request = self.context.get("request")
                if request and hasattr(request, "user"):
                    user = request.user
                    patient = Patient.objects.get(user=user)
                instance.has_reserved = validated_data['has_reserved']
                instance.patient = patient
                instance.reservation_date_time = timezone.now()
                instance.save()
                return instance
            elif instance.has_reserved and not validated_data['has_reserved']:
                instance.has_reserved = validated_data['has_reserved']
                instance.patient = None
                instance.reservation_date_time = None
                instance.save()
                return instance
        except Exception as e:
            raise serializers.ValidationError('Bad Request at: ' + str(e.args))
        raise serializers.ValidationError('Bad Request')
