from datetime import timedelta

from django.utils import timezone

from rest_framework import serializers

from Accounts.models import Doctor
from MedicalHistory.models import MedicalHistory
from TimeReservation.models import AppointmentTime


class MedicalHistorySerializer(serializers.HyperlinkedModelSerializer):
    doctor = serializers.PrimaryKeyRelatedField(read_only=True)
    date = serializers.ReadOnlyField()

    class Meta:
        model = MedicalHistory
        fields = ('url', 'id', 'date', 'content', 'patient', 'doctor')

    def create(self, validated_data):
        try:
            doctor = None
            request = self.context.get("request")
            if request and hasattr(request, "user"):
                user = request.user
                doctor = Doctor.objects.get(user=user)
            validated_data['doctor'] = doctor
            validated_data['date'] = timezone.now().date()
            try:
                AppointmentTime.objects.get(patient=validated_data['patient'], doctor=doctor,
                                            date_time__date=validated_data['date'])
            except AppointmentTime.DoesNotExist:
                raise serializers.ValidationError('You can only enter medical history of your own patients'
                                                  ' you visit today')
            instance = MedicalHistory.objects.create(**validated_data)
            instance.save()
            return instance
        except Exception as e:
            raise serializers.ValidationError('Bad Request at: ' + str(e.args))
