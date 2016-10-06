"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""
import os

import binascii
from django.contrib.auth.models import User
from rest_framework.test import APITestCase

from .models import Settings


class AuthenticationTests(APITestCase):

    def test_authentication(self):
        """
        Ensure we can signup with the api-
        """
        url = ('/api/v1/signup/')
        data = {'username': 'sven', 'email': 'svschannak@gmail.com', 'password': 'test123'}
        response = self.client.post(url, data, format='json')
        current_session_token = Settings.objects.get(user__username='sven').token

        self.assertEqual(current_session_token, response.data)

        url = ('/api/v1/login/')
        data = {'username': 'sven', 'password': 'test123'}
        response = self.client.post(url, data, format='json')
        current_session_token = Settings.objects.get(user__username='sven').token

        self.assertEqual(current_session_token, response.data)


class SnippetTests(APITestCase):

    def setUp(self):
        self.username = "test_user"
        self.email = "test@test.de"
        self.password = "test123"

        self.user = User.objects.create(username=self.username, email=self.email, password=self.password)

        new_token = binascii.b2a_hex(os.urandom(30))
        Settings.objects.create(user=self.user, token=new_token)

        self.token = self.user.settings.token

    def helper_create_snippet(self):
        url = ('/api/v1/snippets/')
        data = {'name': 'Snippet 1', 'content': 'Snippet Content', 'language': 'python'}
        response = self.client.post(url, data, format='json', X_SNIPPET_TOKEN='{}'.format(self.token))
        return response

    def test_create_snippets(self):
        response = self.helper_create_snippet()
        self.assertEqual(response.data, 1)

    def test_get_snippets(self):
        self.helper_create_snippet()
        url = ('/api/v1/snippets/')
        response = self.client.get(url, format='json', X_SNIPPET_TOKEN='{}'.format(self.token))
        self.assertEqual(response.data['results'][0]['name'], 'Snippet 1')

    def test_get_single_snippets(self):
        current_snippet_id = self.helper_create_snippet().data
        url = ('/api/v1/snippets/')
        data = {'snippet_id': current_snippet_id}
        response = self.client.get(url, data, format='json', X_SNIPPET_TOKEN='{}'.format(self.token))
        self.assertEqual(response.data['results'][0]['name'], 'Snippet 1')

    def test_update_snippets(self):
        current_snippet_id = self.helper_create_snippet().data
        url = ('/api/v1/snippets/')
        data = {'name': 'Snippet 2', 'content': 'Snippet Content', 'language': 'python', 'snippet_id': current_snippet_id}
        response_put = self.client.put(url, data, format='json', X_SNIPPET_TOKEN='{}'.format(self.token))

        data = {'snippet_id': current_snippet_id}
        response_get = self.client.get(url, data, format='json', X_SNIPPET_TOKEN='{}'.format(self.token))

        self.assertEqual(response_get.data['results'][0]['name'], 'Snippet 2')

    def test_remove_snippets(self):
        current_snippet_id = self.helper_create_snippet().data
        url = ('/api/v1/snippets/')
        data = {'snippet_id': current_snippet_id}
        response_get = self.client.delete(url, data, format='json', X_SNIPPET_TOKEN='{}'.format(self.token))
        print response_get.data
        self.assertEqual(response_get.data, 'Deleted')




