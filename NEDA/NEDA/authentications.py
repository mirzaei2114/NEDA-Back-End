from rest_framework.authentication import TokenAuthentication, SessionAuthentication, BasicAuthentication


class CsrfExemptTokenAuthentication(TokenAuthentication):

    def enforce_csrf(self, request):
        return  # To not perform the csrf check previously happening


class CsrfExemptSessionAuthentication(SessionAuthentication):

    def enforce_csrf(self, request):
        return  # To not perform the csrf check previously happening


class CsrfExemptBasicAuthentication(BasicAuthentication):

    def enforce_csrf(self, request):
        return  # To not perform the csrf check previously happening

