from rest_framework import serializers

from Accounts.models import Doctor, Hospital, Patient
from RateAndComment import models
from RateAndComment.models import DoctorComment, DoctorRate, HospitalRate, HospitalComment, ClinicRate, ClinicComment
from TimeReservation.models import AppointmentTime


class DoctorRateSerializer(serializers.ModelSerializer):
    patient = serializers.PrimaryKeyRelatedField(read_only=True)

    def create(self, validated_data):
        try:
            request = self.context.get("request")
            user = request.user
            patient = Patient.objects.get(user=user)
            try:
                instance = DoctorRate.objects.get(patient=patient)
                instance.rate = validated_data['rate']
            except DoctorRate.DoesNotExist:
                validated_data['patient'] = patient
                instance = DoctorRate.objects.create(**validated_data)
            instance.save()
        except Exception as e:
            raise serializers.ValidationError('Bad Request at: ' + str(e.args))
        return instance

    def validate(self, attrs):
        if 5 <= attrs['rate'] or attrs['rate'] <= 0:
            raise serializers.ValidationError('Rate must be between 0 and 5')

        request = self.context.get("request")
        user = request.user
        patient = Patient.objects.get(user=user)
        try:
            AppointmentTime.objects.get(patient=patient, doctor=attrs['doctor'])
        except AppointmentTime.DoesNotExist:
            raise serializers.ValidationError('You can rate only doctors you have visited by')
        return super().validate(attrs)

    class Meta:
        model = DoctorRate
        fields = ('url', 'id', 'doctor', 'patient', 'rate')


class DoctorCommentSerializer(serializers.ModelSerializer):
    patient = serializers.PrimaryKeyRelatedField(read_only=True)

    def create(self, validated_data):
        try:
            request = self.context.get("request")
            user = request.user
            patient = Patient.objects.get(user=user)
            validated_data['patient'] = patient
            instance = DoctorComment.objects.create(**validated_data)
            instance.save()
        except Exception as e:
            raise serializers.ValidationError('Bad Request at: ' + str(e.args))
        return instance

    def validate(self, attrs):
        request = self.context.get("request")
        user = request.user
        patient = Patient.objects.get(user=user)
        try:
            AppointmentTime.objects.get(patient=patient, doctor=attrs['doctor'])
        except AppointmentTime.DoesNotExist:
            raise serializers.ValidationError('You can left comment only about doctors you have visited by')
        return super().validate(attrs)

    class Meta:
        model = DoctorComment
        fields = ('url', 'id', 'doctor', 'patient', 'comment')


class HospitalRateSerializer(serializers.ModelSerializer):
    patient = serializers.PrimaryKeyRelatedField(read_only=True)

    def create(self, validated_data):
        try:
            request = self.context.get("request")
            user = request.user
            patient = Patient.objects.get(user=user)
            try:
                instance = HospitalRate.objects.get(patient=patient)
                instance.rate = validated_data['rate']
            except HospitalRate.DoesNotExist:
                validated_data['patient'] = patient
                instance = HospitalRate.objects.create(**validated_data)
            instance.save()
        except Exception as e:
            raise serializers.ValidationError('Bad Request at: ' + str(e.args))
        return instance

    def validate(self, attrs):
        if 5 <= attrs['rate'] or attrs['rate'] <= 0:
            raise serializers.ValidationError('Rate must be between 0 and 5')

        request = self.context.get("request")
        user = request.user
        patient = Patient.objects.get(user=user)
        try:
            AppointmentTime.objects.get(patient=patient, hospital=attrs['hospital'])
        except AppointmentTime.DoesNotExist:
            raise serializers.ValidationError('You can rate only hospitals you have visited by a doctor at it')
        return super().validate(attrs)

    class Meta:
        model = HospitalRate
        fields = ('url', 'id', 'hospital', 'patient', 'rate')


class HospitalCommentSerializer(serializers.ModelSerializer):
    patient = serializers.PrimaryKeyRelatedField(read_only=True)

    def create(self, validated_data):
        try:
            request = self.context.get("request")
            user = request.user
            patient = Patient.objects.get(user=user)
            validated_data['patient'] = patient
            instance = HospitalComment.objects.create(**validated_data)
            instance.save()
        except Exception as e:
            raise serializers.ValidationError('Bad Request at: ' + str(e.args))
        return instance

    def validate(self, attrs):
        request = self.context.get("request")
        user = request.user
        patient = Patient.objects.get(user=user)
        try:
            AppointmentTime.objects.get(patient=patient, hospital=attrs['hospital'])
        except AppointmentTime.DoesNotExist:
            raise serializers.ValidationError('You can left comment only about hospitals you have visited by a doctor'
                                              ' at it')
        return super().validate(attrs)

    class Meta:
        model = HospitalComment
        fields = ('url', 'id', 'hospital', 'patient', 'comment')


class ClinicRateSerializer(serializers.ModelSerializer):
    patient = serializers.PrimaryKeyRelatedField(read_only=True)

    def create(self, validated_data):
        try:
            request = self.context.get("request")
            user = request.user
            patient = Patient.objects.get(user=user)
            try:
                instance = ClinicRate.objects.get(patient=patient)
                instance.rate = validated_data['rate']
            except ClinicRate.DoesNotExist:
                validated_data['patient'] = patient
                instance = ClinicRate.objects.create(**validated_data)
            instance.save()
        except Exception as e:
            raise serializers.ValidationError('Bad Request at: ' + str(e.args))
        return instance

    def validate(self, attrs):
        if 5 <= attrs['rate'] or attrs['rate'] <= 0:
            raise serializers.ValidationError('Rate must be between 0 and 5')

        request = self.context.get("request")
        user = request.user
        patient = Patient.objects.get(user=user)
        try:
            AppointmentTime.objects.get(patient=patient, clinic=attrs['clinic'])
        except AppointmentTime.DoesNotExist:
            raise serializers.ValidationError('You can rate only clinics you have visited by a doctor at it')
        return super().validate(attrs)

    class Meta:
        model = ClinicRate
        fields = ('url', 'id', 'clinic', 'patient', 'rate')


class ClinicCommentSerializer(serializers.ModelSerializer):
    patient = serializers.PrimaryKeyRelatedField(read_only=True)

    def create(self, validated_data):
        try:
            request = self.context.get("request")
            user = request.user
            patient = Patient.objects.get(user=user)
            validated_data['patient'] = patient
            instance = ClinicComment.objects.create(**validated_data)
            instance.save()
        except Exception as e:
            raise serializers.ValidationError('Bad Request at: ' + str(e.args))
        return instance

    def validate(self, attrs):
        request = self.context.get("request")
        user = request.user
        patient = Patient.objects.get(user=user)
        try:
            AppointmentTime.objects.get(patient=patient, clinic=attrs['clinic'])
        except AppointmentTime.DoesNotExist:
            raise serializers.ValidationError('You can left comment only about clinics you have visited by a doctor'
                                              ' at it')
        return super().validate(attrs)

    class Meta:
        model = ClinicComment
        fields = ('url', 'id', 'clinic', 'patient', 'comment')
