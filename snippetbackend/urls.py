from django.conf.urls import url, include
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()
from rest_framework import routers
from api.api.views.authentication import LoginView, SignUpView
from api.api.views.snippets import SnippetView

urlpatterns = [
    url(r'^api/v1/login/$', LoginView.as_view(), name='login'),
    url(r'^api/v1/signup/$', SignUpView.as_view(), name='signup'),
    url(r'^api/v1/snippets/$', SnippetView.as_view(), name='snippets'),
]

