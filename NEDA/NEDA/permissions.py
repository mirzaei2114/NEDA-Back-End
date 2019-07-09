from rest_framework import permissions

from Accounts.models import Doctor, Patient


class IsSameUserSuperuserOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow user to edit his/her instance.
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        return (request.user.is_authenticated and request.user.is_superuser) or (
            obj == request.user and request.method in ('PUT', 'DELETE'))


class IsOwnerSuperuserOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owner of an object to edit it.
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        return (request.user.is_authenticated and request.user.is_superuser) or (
            obj.user == request.user and request.method in ('PUT', 'DELETE'))


class IsNotAuthenticated(permissions.BasePermission):
    def has_permission(self, request, view):
        return not request.user.is_authenticated
      

class IsSameDoctorIsDoctorOrReadonly(permissions.BasePermission):
    """
    Custom permission to only allow a doctor to create and edit his/her own clinics and readonly for others
    """
    def has_permission(self, request, view):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        return request.user.is_authenticated and request.user.is_doctor

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        if not (request.user.is_authenticated and request.user.is_doctor):
            return False

        doctor = Doctor.objects.get(user=request.user)

        return request.method == 'POST' or (obj.doctor == doctor and request.method in ('PUT', 'DELETE'))


class ReserveTimePermission(permissions.BasePermission):
    """
    Custom permission to only allow a patient to reserve or cancel his/her own time and readonly for others
    """
    """
    Custom permission to only allow an authenticated user to create an object and an owner to edit his/her object
    """
    def has_permission(self, request, view):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS or request.user.is_superuser:
            return True

        if request.user.is_patient:
            patient = Patient.objects.get(user=request.user)
            return not obj.has_reserved or (obj.has_reserved and obj.patient == patient)
        elif request.user.is_doctor:
            doctor = Doctor.objects.get(user=request.user)
            return obj.has_reserved and obj.doctor == doctor
        return False


class IsSamePatientAuthenticatedOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow an authenticated user to create an object and an owner to edit his/her object
    """
    def has_permission(self, request, view):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        return request.user.is_authenticated and request.user.is_patient

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS or ((request.user.is_staff or request.user.is_superuser)
                                                          and request.method == 'DELETE'):
            return True

        patient = Patient.objects.get(user=request.user)
        return obj.patient == patient


class TransactionPermission(permissions.BasePermission):
    """
    Custom permission to only allow owner of an object to edit it.
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        if not (request.user.is_authenticated and request.user.is_patient):
            return False

        patient = Patient.objects.get(user=request.user)
        return request.method == 'PUT' and obj.appointment_time.patient == patient
