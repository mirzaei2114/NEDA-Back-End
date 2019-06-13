from rest_framework import viewsets, mixins
from NEDA.permissions import IsSameUserSuperuserOrReadOnly, IsOwnerSuperuserOrReadOnly, IsNotAuthenticated
from .models import MyUser, Patient, Doctor, Hospital
from .serializers import UserSerializer, PatientSerializer, DoctorSerializer, HospitalSerializer


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = (IsSameUserSuperuserOrReadOnly,)
    queryset = MyUser.objects.all()
    serializer_class = UserSerializer


class PatientViewSet(mixins.UpdateModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin,
                     viewsets.GenericViewSet):
    permission_classes = (IsOwnerSuperuserOrReadOnly,)
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer


class DoctorViewSet(mixins.UpdateModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin,
                    viewsets.GenericViewSet):
    permission_classes = (IsOwnerSuperuserOrReadOnly,)
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer


class HospitalViewSet(mixins.UpdateModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin,
                      viewsets.GenericViewSet):
    permission_classes = (IsOwnerSuperuserOrReadOnly,)
    queryset = Hospital.objects.all()
    serializer_class = HospitalSerializer

