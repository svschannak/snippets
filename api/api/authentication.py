from django.contrib.auth.models import User
from rest_framework import authentication
from rest_framework import exceptions

from api.models import Settings


class TokenAuthentication(authentication.BaseAuthentication):

    def authenticate(self, request):
        token = request.META.get('X_SNIPPET_TOKEN', request.GET['token'])

        if not token:
            print request.GET
            return None

        try:
            print token
            user = Settings.objects.get(token=token).user
        except Settings.DoesNotExist:
            raise exceptions.AuthenticationFailed('No such user')

        return (user, None)