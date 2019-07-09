from django.utils import timezone
from rest_framework import serializers

from RateAndComment.serializers import DoctorRateSerializer, DoctorCommentSerializer, HospitalRateSerializer, \
    HospitalCommentSerializer
from TimeReservation.models import Clinic
from .models import MyUser, Patient, Doctor, Hospital


class UserSerializer(serializers.HyperlinkedModelSerializer):
    social_number = serializers.CharField(max_length=10, required=False)
    gender = serializers.CharField(max_length=3, required=False)
    phone_number = serializers.CharField(max_length=8, required=False)
    mobile_number = serializers.CharField(help_text='Like 09XXXXXXXXX', max_length=11, required=False)
    address = serializers.CharField(max_length=512, required=False)

    medical_system_number = serializers.CharField(max_length=50, required=False)
    expertise = serializers.CharField(max_length=50, required=False)

    post_code = serializers.CharField(max_length=10, required=False)

    def create(self, validated_data):
        user = None
        patient = None
        doctor = None
        hospital = None
        if validated_data['is_patient'] and not validated_data['is_doctor'] and not validated_data['is_hospital']:
            user = MyUser.objects.create(
                first_name=validated_data['first_name'],
                last_name=validated_data['last_name'],
                username=validated_data['username'],
                email=validated_data['email'],
                is_patient=validated_data['is_patient'],
                is_doctor=validated_data['is_doctor'],
                is_hospital=validated_data['is_hospital'],
                date_joined=timezone.now()
            )
            try:
                user.set_password(validated_data['password'])
                user.save()
                patient = Patient.objects.create(
                    user_id=user.id,
                    social_number=validated_data['social_number'],
                    gender=validated_data['gender'],
                    mobile_number=validated_data['mobile_number'],
                )
                patient.save()
            except Exception as e:
                user.delete()
                if patient:
                    patient.delete()
                raise serializers.ValidationError('Bad request at: ' + str(e.args))

        elif not validated_data['is_patient'] and validated_data['is_doctor'] and not validated_data['is_hospital']:
            user = MyUser.objects.create(
                first_name=validated_data['first_name'],
                last_name=validated_data['last_name'],
                username=validated_data['username'],
                email=validated_data['email'],
                province=validated_data['province'],
                is_patient=validated_data['is_patient'],
                is_doctor=validated_data['is_doctor'],
                is_hospital=validated_data['is_hospital'],
                date_joined=timezone.now()
            )
            try:
                user.set_password(validated_data['password'])
                user.save()
                doctor = Doctor.objects.create(
                    user_id=user.id,
                    medical_system_number=validated_data['medical_system_number'],
                    gender=validated_data['gender'],
                    expertise=validated_data['expertise'],
                    mobile_number=validated_data['mobile_number'],
                )
                doctor.save()
            except Exception as e:
                user.delete()
                if doctor:
                    doctor.delete()
                raise serializers.ValidationError('Bad request at: ' + str(e.args))

        elif not validated_data['is_patient'] and not validated_data['is_doctor'] and validated_data['is_hospital']:
            user = MyUser.objects.create(
                first_name=validated_data['first_name'],
                username=validated_data['username'],
                email=validated_data['email'],
                province=validated_data['province'],
                is_patient=validated_data['is_patient'],
                is_doctor=validated_data['is_doctor'],
                is_hospital=validated_data['is_hospital'],
                date_joined=timezone.now()
            )
            try:
                user.set_password(validated_data['password'])
                user.save()
                hospital = Hospital.objects.create(
                    user_id=user.id,
                    post_code=validated_data['post_code'],
                    phone_number=validated_data['phone_number'],
                    address=validated_data['address'],
                )
                hospital.save()
            except Exception as e:
                user.delete()
                if hospital:
                    hospital.delete()
                raise serializers.ValidationError('Bad request at: ' + str(e.args))
        if not user:
            raise serializers.ValidationError('Bad request at user information')
        return user

    def update(self, instance, validated_data):
        try:
            instance.first_name = validated_data['first_name']
            instance.last_name = validated_data['last_name']
            instance.username = validated_data['username']
            if 'province' in validated_data:
                instance.province = validated_data['province']
            instance.email = validated_data['email']
            instance.is_patient = validated_data['is_patient']
            instance.is_doctor = validated_data['is_doctor']
            instance.is_hospital = validated_data['is_hospital']
            instance.set_password(validated_data['password'])
            instance.save()
        except Exception as e:
            raise serializers.ValidationError('Bad Request at: ' + str(e.args))
        return instance

    class Meta:
        model = MyUser
        fields = ('url', 'id', 'first_name', 'last_name', 'username', 'password', 'mobile_number',
                  'province', 'email', 'is_doctor', 'is_patient', 'is_hospital',
                  'social_number', 'gender', 'phone_number', 'address',
                  'medical_system_number', 'expertise', 'post_code',)

    def validate(self, attrs):
        if [attrs['is_patient'], attrs['is_doctor'], attrs['is_hospital']].count(True) != 1:
            raise serializers.ValidationError('A user can be one of patient, doctor or hospital')
        return super().validate(attrs)


class InnerUserSerializer(serializers.HyperlinkedModelSerializer):
    username = serializers.CharField(read_only=True)

    class Meta:
        model = MyUser
        fields = ('url', 'username', 'password', 'first_name', 'last_name', 'email', 'province')

    @staticmethod
    def update_user(validated_data, user):
        user = MyUser.objects.get(id=user.id)
        previous_info = {'first_name': user.first_name, 'last_name': user.last_name, 'email': user.email,
                         'password': user.password, 'province': user.province}
        try:
            user_info = validated_data.pop('user')
            user.first_name = user_info['first_name']
            user.last_name = user_info['last_name']
            user.email = user_info['email']
            user.province = user_info['province']
            if user.password != user_info['password']:
                user.set_password(user_info['password'])
            user.save()
        except Exception as e:
            InnerUserSerializer.rollback_user(user, previous_info)
            raise serializers.ValidationError('Bad request at: ' + str(e.args))

        return user, previous_info

    @staticmethod
    def rollback_user(user, previous_info):
        user.first_name = previous_info['first_name']
        user.last_name = previous_info['last_name']
        user.email = previous_info['email']
        user.province = previous_info['province']
        user.password = previous_info['password']
        user.save()


class PatientSerializer(serializers.HyperlinkedModelSerializer):
    user = InnerUserSerializer()
    wallet = serializers.ReadOnlyField()

    class Meta:
        model = Patient
        fields = ('url', 'user', 'social_number', 'gender', 'mobile_number', 'phone_number', 'address', 'date_of_birth',
                  'picture', 'patient_appointment_times', 'wallet')
        depth = 1

    def update(self, instance, validated_data):
        user, previous_info = InnerUserSerializer.update_user(validated_data, instance.user)
        try:
            instance.user = user
            instance.social_number = validated_data['social_number']
            instance.gender = validated_data['gender']
            instance.mobile_number = validated_data['mobile_number']
            instance.phone_number = validated_data['phone_number']
            instance.address = validated_data['address']
            instance.date_of_birth = validated_data['date_of_birth']
            if 'picture' in validated_data.keys():
                instance.picture = validated_data['picture']
            instance.save()
        except Exception as e:
            InnerUserSerializer.rollback_user(user, previous_info)
            raise serializers.ValidationError('Bad request at: ' + str(e.args))

        return instance


class DoctorSerializer(serializers.HyperlinkedModelSerializer):
    user = InnerUserSerializer()
    doctor_rates = DoctorRateSerializer(many=True, read_only=True)
    doctor_comments = DoctorCommentSerializer(many=True, read_only=True)
    rate = serializers.ReadOnlyField()
    rate_number = serializers.ReadOnlyField()

    class Meta:
        model = Doctor
        fields = ('url', 'user', 'gender', 'medical_system_number', 'expertise', 'date_of_birth', 'mobile_number',
                  'bio', 'picture', 'doctor_clinics', 'hospitals', 'doctor_rates', 'doctor_comments',
                  'rate', 'rate_number')
        depth = 1

    def update(self, instance, validated_data):
        user, previous_info = InnerUserSerializer.update_user(validated_data, instance.user)
        try:
            instance.user = user
            instance.gender = validated_data['gender']
            instance.medical_system_number = validated_data['medical_system_number']
            instance.expertise = validated_data['expertise']
            instance.date_of_birth = validated_data['date_of_birth']
            instance.mobile_number = validated_data['mobile_number']
            instance.bio = validated_data['bio']
            if 'picture' in validated_data.keys():
                instance.picture = validated_data['picture']
            instance.save()
        except Exception as e:
            InnerUserSerializer.rollback_user(user, previous_info)
            raise serializers.ValidationError('Bad request at: ' + str(e.args))

        return instance


class HospitalSerializer(serializers.HyperlinkedModelSerializer):
    user = InnerUserSerializer()
    hospital_rates = HospitalRateSerializer(many=True, read_only=True)
    hospital_comments = HospitalCommentSerializer(many=True, read_only=True)
    rate = serializers.ReadOnlyField()
    rate_number = serializers.ReadOnlyField()

    class Meta:
        model = Hospital
        fields = ('url', 'user', 'phone_number', 'address', 'post_code', 'doctors', 'bio', 'picture', 'hospital_rates',
                  'hospital_comments', 'rate', 'rate_number')
        depth = 1

    def update(self, instance, validated_data):
        user, previous_info = InnerUserSerializer.update_user(validated_data, instance.user)
        try:

            instance.user = user
            instance.phone_number = validated_data['phone_number']
            instance.address = validated_data['address']
            instance.post_code = validated_data['post_code']
            instance.doctors.set(validated_data['doctors'])
            instance.bio = validated_data['bio']
            if 'picture' in validated_data.keys():
                instance.picture = validated_data['picture']
            instance.save()
        except Exception as e:
            InnerUserSerializer.rollback_user(user, previous_info)
            raise serializers.ValidationError('Bad request at: ' + str(e.args))

        return instance
