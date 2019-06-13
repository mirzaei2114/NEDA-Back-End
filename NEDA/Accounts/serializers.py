from django.db import transaction
from django.utils import timezone
from rest_framework import serializers
from .models import MyUser, Patient, Doctor, Hospital


class UserSerializer(serializers.HyperlinkedModelSerializer):
    social_number = serializers.CharField(max_length=10, required=False)
    gender = serializers.BooleanField(required=False)
    phone_number = serializers.CharField(max_length=8, required=False)
    mobile_number = serializers.CharField(help_text='Like 09XXXXXXXXX', max_length=11, required=False)
    address = serializers.CharField(max_length=512, required=False)
    date_of_birth = serializers.DateField(required=False)

    medical_system_number = serializers.CharField(max_length=50,required=False)
    expertise = serializers.CharField(max_length=50, required=False)

    post_code = serializers.CharField(max_length=10, required=False)

    def create(self, validated_data):
        user = None
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
            user.set_password(validated_data['password'])
            patient = Patient.objects.create(
                user_id=user.id,
                social_number=validated_data['social_number'],
                gender=validated_data['gender'],
                mobile_number=validated_data['mobile_number'],
            )
            try:
                patient.save()
                user.save()
            except:
                patient.delete()
                patient.save()
                user.delete()
                user.save()
        elif not validated_data['is_patient'] and validated_data['is_doctor'] and not validated_data['is_hospital']:
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
            user.set_password(validated_data['password'])
            doctor = Doctor.objects.create(
                user_id=user.id,
                medical_system_number=validated_data['medical_system_number'],
                gender=validated_data['gender'],
                date_of_birth=validated_data['date_of_birth'],
                expertise=validated_data['expertise'],
                mobile_number=validated_data['mobile_number'],
            )
            try:
                doctor.save()
                user.save()
            except:
                doctor.delete()
                user.delete()
                doctor.save()
                user.save()
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
            user.set_password(validated_data['password'])
            hospital = Hospital.objects.create(
                user_id=user.id,
                post_code=validated_data['post_code'],
                phone_number=validated_data['phone_number'],
                address=validated_data['address'],
            )
            try:
                hospital.save()
                user.save()
            except:
                hospital.delete()
                user.delete()
                hospital.save()
                user.save()
        if user:
            return user

    class Meta:
        model = MyUser
        fields = ('url', 'id', 'first_name', 'last_name', 'username', 'password', 'mobile_number',
                  'province', 'email', 'is_doctor', 'is_patient', 'is_hospital',
                  'social_number', 'gender', 'phone_number', 'address', 'date_of_birth',
                  'medical_system_number', 'expertise', 'post_code',)

#
# class MyRelatedField(serializers.RelatedField):
#     def to_internal_value(self, data):
#         return data
#
#     def to_representation(self, value):
#         return value
#


class PatientSerializer(serializers.HyperlinkedModelSerializer):
    # user = serializers.HyperlinkedRelatedField(many=False, view_name='myuser-detail', read_only=True)
    first_name = serializers.ReadOnlyField(source='user.first_name')
    last_name = serializers.ReadOnlyField(source='user.last_name')
    username = serializers.ReadOnlyField(source='user.username')
    password = serializers.ReadOnlyField(source='user.password')
    email = serializers.ReadOnlyField(source='user.email')

    class Meta:
        model = Patient
        fields = ('url', 'first_name', 'last_name', 'gender', 'username', 'password', 'email', 'social_number',
                  'phone_number', 'mobile_number', 'address', 'date_of_birth', 'picture')


class DoctorSerializer(serializers.HyperlinkedModelSerializer):
    # user = serializers.HyperlinkedRelatedField(many=False, view_name='myuser-detail', read_only=True)
    first_name = serializers.ReadOnlyField(source='user.first_name')
    last_name = serializers.ReadOnlyField(source='user.last_name')
    username = serializers.ReadOnlyField(source='user.username')
    password = serializers.ReadOnlyField(source='user.password')
    email = serializers.ReadOnlyField(source='user.email')

    class Meta:
        model = Doctor
        fields = ('url', 'first_name', 'last_name', 'gender', 'username', 'password', 'email',
                  'medical_system_number', 'date_of_birth', 'expertise', 'bio', 'picture')


class HospitalSerializer(serializers.HyperlinkedModelSerializer):
    # user = serializers.HyperlinkedRelatedField(many=False, view_name='myuser-detail', read_only=True)
    name = serializers.ReadOnlyField(source='user.first_name')
    username = serializers.ReadOnlyField(source='user.username')
    password = serializers.ReadOnlyField(source='user.password')
    email = serializers.ReadOnlyField(source='user.email')

    class Meta:
        model = Hospital
        fields = ('url', 'name', 'username', 'password', 'email', 'phone_number', 'address', 'post_code', 'doctors',
                  'bio', 'picture')
