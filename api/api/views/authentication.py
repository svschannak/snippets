from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
import os, binascii
from django.db import IntegrityError
from django.contrib.auth import authenticate

from api.models import Settings


class LoginView(APIView):
    """
    Login to the rest api with e-mail address and password.

    If login was successful, it returns a user token.
    If login was not successful, it returns an error-description.
    """

    def post(self, request, format=None):
        user = authenticate(username=request.data['username'], password=request.data['password'])

        if user:
            new_token = binascii.b2a_hex(os.urandom(30))
            user.settings.token = new_token
            user.settings.save()

            return Response(new_token)

        else:

            # TODO: Add error handler for login
            return Response('Not logged in')


class SignUpView(APIView):
    """
    Login to the rest api with e-mail address and password.

    If login was successful, it returns a user token.
    If login was not successful, it returns an error-description.
    """

    def post(self, request, format=None):
        try:
            user = User.objects.create_user(request.POST['username'], request.POST['email'], request.POST['password'])

            settings = Settings.objects.create(user=user)

            settings.token = binascii.b2a_hex(os.urandom(30))
            settings.save()

            return Response(settings.token)

        except IntegrityError, e:
            # TODO: Add Error handling for signup
            return Response(e)

