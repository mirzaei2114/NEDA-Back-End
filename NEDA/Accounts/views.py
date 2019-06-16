from rest_framework import viewsets, mixins, status
from rest_framework.response import Response

from NEDA.permissions import IsSameUserSuperuserOrReadOnly, IsOwnerSuperuserOrReadOnly, IsNotAuthenticated
from .models import MyUser, Patient, Doctor, Hospital
from .serializers import UserSerializer, PatientSerializer, DoctorSerializer, HospitalSerializer


class UserViewSet(mixins.CreateModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    permission_classes = (IsSameUserSuperuserOrReadOnly,)
    queryset = MyUser.objects.all()
    serializer_class = UserSerializer


class PatientViewSet(mixins.UpdateModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin,
                     mixins.DestroyModelMixin, viewsets.GenericViewSet):
    permission_classes = (IsOwnerSuperuserOrReadOnly,)
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        # self.perform_destroy(instance.user)
        # self.perform_destroy(instance)
        instance.user.is_active = False
        instance.user.save()
        return Response(instance, status.HTTP_202_ACCEPTED)


class DoctorViewSet(mixins.UpdateModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin,
                    mixins.DestroyModelMixin, viewsets.GenericViewSet):
    permission_classes = (IsOwnerSuperuserOrReadOnly,)
    queryset = Doctor.objects.all()
    serializer_class = DoctorSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        # self.perform_destroy(instance.user)
        # self.perform_destroy(instance)
        instance.user.is_active = False
        instance.user.save()
        return Response(instance, status.HTTP_202_ACCEPTED)


class HospitalViewSet(mixins.UpdateModelMixin, mixins.ListModelMixin, mixins.RetrieveModelMixin,
                      mixins.DestroyModelMixin, viewsets.GenericViewSet):
    permission_classes = (IsOwnerSuperuserOrReadOnly,)
    queryset = Hospital.objects.all()
    serializer_class = HospitalSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        # self.perform_destroy(instance.user)
        # self.perform_destroy(instance)
        instance.user.is_active = False
        instance.user.save()
        return Response(instance, status.HTTP_202_ACCEPTED)


