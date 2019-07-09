from django.utils import timezone
from datetime import timedelta, datetime

from rest_framework import serializers
from Accounts.models import Doctor, Patient, Hospital
from RateAndComment.serializers import ClinicRateSerializer, ClinicCommentSerializer
from TimeReservation.models import Clinic, WorkingHour, AppointmentTime, DAYS_PER, Bonus, Transaction


class ClinicSerializer(serializers.HyperlinkedModelSerializer):
    doctor = serializers.PrimaryKeyRelatedField(read_only=True)
    clinic_rates = ClinicRateSerializer(many=True, read_only=True)
    clinic_comments = ClinicCommentSerializer(many=True, read_only=True)
    rate = serializers.ReadOnlyField()
    rate_number = serializers.ReadOnlyField()

    class Meta:
        model = Clinic
        fields = ('url', 'id', 'name', 'province', 'phone_number', 'address', 'doctor', 'clinic_rates',
                  'clinic_comments', 'rate', 'rate_number')

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


class TransactionSerializer(serializers.HyperlinkedModelSerializer):
    price = serializers.ReadOnlyField()
    date_time = serializers.ReadOnlyField()
    appointment_time = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Transaction
        fields = ('url', 'id', 'price', 'card_number', 'date_time', 'success', 'appointment_time')

    def update(self, instance, validated_data):
        try:
            if not instance.success and validated_data['success']:
                instance.success = True
                instance.date_time = timezone.now()
                instance.card_number = validated_data['card_number']
                instance.appointment_time.has_paid = True
                instance.appointment_time.save()
                instance.save()
                return instance
        except Exception as e:
            raise serializers.ValidationError('Bad Request at: ' + str(e.args))


class AppointmentTimeSerializer(serializers.HyperlinkedModelSerializer):
    doctor = serializers.PrimaryKeyRelatedField(read_only=True)
    patient = serializers.PrimaryKeyRelatedField(read_only=True)
    reservation_date_time = serializers.DateTimeField(read_only=True)
    clinic = serializers.PrimaryKeyRelatedField(read_only=True)
    hospital = serializers.PrimaryKeyRelatedField(read_only=True)
    price = serializers.ReadOnlyField()
    total_price = serializers.ReadOnlyField()
    date_time = serializers.PrimaryKeyRelatedField(read_only=True)
    bonus_amount = serializers.ReadOnlyField()
    has_paid = serializers.ReadOnlyField()
    appointment_time_transaction = TransactionSerializer(read_only=True)
    visitation_time = serializers.ReadOnlyField()

    class Meta:
        model = AppointmentTime
        fields = ('url', 'id', 'date_time', 'reservation_date_time', 'has_reserved', 'has_paid', 'price', 'bonus_amount'
                  , 'total_price', 'doctor', 'patient', 'clinic', 'hospital', 'appointment_time_transaction',
                  'visiting', 'visited', 'visitation_time',)

    def validate(self, attrs):
        request = self.context.get("request")
        user = request.user
        if user.is_patient and (attrs['visiting'] or attrs['visited']):
            raise serializers.ValidationError('You can not do this!')
        return super().validate(attrs)

    def update(self, instance, validated_data):
        try:

            if instance.has_reserved and not instance.visiting and validated_data['visiting']:
                instance.visiting = True
                instance.save()
                return instance
            elif instance.has_reserved and instance.visiting and not instance.visited and validated_data['visited']:
                instance.visiting = False
                instance.visited = True
                instance.visitation_time = timezone.now().time()
                instance.save()
                return instance
            elif not instance.has_reserved and validated_data['has_reserved'] and not validated_data['visiting'] \
                    and not validated_data['visited']:
                patient = None
                request = self.context.get("request")
                if request and hasattr(request, "user"):
                    user = request.user
                    patient = Patient.objects.get(user=user)
                instance.has_reserved = validated_data['has_reserved']
                instance.patient = patient
                instance.reservation_date_time = timezone.now()

                try:
                    bonus = Bonus.objects.get(doctor=instance.doctor, patient=patient)
                    if instance.price - bonus.amount >= 0:
                        total_price = instance.price - bonus.amount
                        instance.bonus_amount = bonus.amount
                        bonus.delete()
                    else:
                        total_price = 0
                        bonus.amount -= instance.price
                        instance.bonus_amount = instance.price
                        bonus.save()
                except Bonus.DoesNotExist:
                    total_price = instance.price

                if instance.patient.wallet > 0:
                    if instance.patient.wallet > total_price:
                        instance.patient.wallet -= total_price
                        total_price = 0
                    else:
                        total_price = total_price - instance.patient.wallet
                        instance.patient.wallet = 0

                instance.patient.save()
                instance.total_price = total_price
                instance.save()
                Transaction.objects.create(appointment_time=instance, price=total_price)
                return instance
            elif instance.has_reserved and not validated_data['has_reserved'] and not validated_data['visiting'] \
                    and not validated_data['visited']:
                request = self.context.get("request")
                user = request.user
                if user.is_patient:
                    instance.has_reserved = validated_data['has_reserved']
                    if instance.bonus_amount > 0:
                        try:
                            bonus = Bonus.objects.get(doctor=instance.doctor, patient=instance.patient)
                            bonus.amount += instance.bonus_amount
                            bonus.save()
                        except Bonus.DoesNotExist:
                            bonus = Bonus.objects.create(patient=instance.patient, doctor=instance.doctor,
                                                         amount=instance.bonus_amount)
                            bonus.save()
                        instance.patient.wallet += instance.price - instance.bonus_amount
                        instance.patient.save()
                    else:
                        instance.patient.wallet += instance.price
                        instance.patient.save()
                    instance.bonus_amount = 0
                    instance.patient = None
                    instance.reservation_date_time = None
                    instance.total_price = 0
                    instance.save()
                    return instance
                elif user.is_doctor:
                    doctor = Doctor.objects.get(user=user)
                    instance.has_reserved = validated_data['has_reserved']
                    had_bonus = False
                    if instance.bonus_amount > 0:
                        try:
                            bonus = Bonus.objects.get(doctor=instance.doctor, patient=instance.patient)
                            bonus.amount += instance.bonus_amount
                            had_bonus = True
                            bonus.save()
                        except Bonus.DoesNotExist:
                            bonus = Bonus.objects.create(patient=instance.patient, doctor=instance.doctor,
                                                         amount=instance.bonus_amount)
                            bonus.save()
                        instance.patient.wallet += instance.price - instance.bonus_amount
                        instance.patient.save()
                    else:
                        instance.patient.wallet += instance.price
                        instance.patient.save()
                    bonus_amount = instance.bonus_amount
                    instance.bonus_amount = 0
                    patient = instance.patient
                    instance.patient = None
                    reservation_date_time = instance.reservation_date_time
                    instance.reservation_date_time = None
                    total_price = instance.total_price
                    instance.total_price = 0
                    instance.save()
                    try:
                        amount = 0.1 * instance.price
                        try:
                            bonus = Bonus.objects.get(doctor=doctor, patient=patient)
                            bonus.amount += amount
                            bonus.save()
                        except Bonus.DoesNotExist:
                            data = {'amount': amount, 'doctor': doctor, 'patient': patient}
                            bonus = Bonus.objects.create(**data)
                            bonus.save()
                        return instance
                    except Exception as e:
                        if not had_bonus:
                            bonus.delete()
                        instance.bonus_amount = bonus_amount
                        instance.patient = patient
                        instance.reservation_date_time = reservation_date_time
                        instance.has_reserved = True
                        instance.total_price = total_price
                        instance.save()
                        raise serializers.ValidationError('Bad Request at: ' + str(e.args))
        except Exception as e:
            raise serializers.ValidationError('Bad Request at: ' + str(e.args))
        raise serializers.ValidationError('Bad Request')


class BonusSerializer(serializers.HyperlinkedModelSerializer):
    doctor = serializers.PrimaryKeyRelatedField(many=False, read_only=True)
    patient = serializers.PrimaryKeyRelatedField(many=False, read_only=True)
    amount = serializers.ReadOnlyField()

    class Meta:
        model = Bonus
        fields = ('url', 'id', 'amount', 'doctor', 'patient')

