from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response


class GetToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        if user.is_patient:
            return Response({'token': token.key, 'kind': 'patient'})
        elif user.is_doctor:
            return Response({'token': token.key, 'kind': 'doctor'})
        elif user.is_hospital:
            return Response({'token': token.key, 'kind': 'hospital'})
        else:
            return Response({'token': token.key, 'kind': 'admin'})

