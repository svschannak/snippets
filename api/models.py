from django.db import models
from django.contrib.auth.models import User


class Settings(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=250)


class Snippet(models.Model):
    name = models.CharField(max_length=255)
    content = models.TextField()
    language = models.CharField(max_length=255)

    created_by = models.ForeignKey(User, related_name="created_snippets")
    updated_by = models.ForeignKey(User, related_name="updated_snippets")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        permissions = (
            ('view_snippet', 'View Snippet'),
            ('edit_snippet', 'Edit Snippet')
        )

class SnippetHistory(models.Model):
    origin = models.ForeignKey(Snippet)
    name = models.CharField(max_length=255)
    content = models.TextField()
    language = models.CharField(max_length=255)

    created_by = models.ForeignKey(User, related_name="changed_snippets")

    created_at = models.DateTimeField(auto_now_add=True)


class SnippetLibrary(models.Model):
    snippets = models.ManyToManyField(Snippet)
    created_by = models.ForeignKey(User, related_name="created_libraries")

# TODO:
# Comments
# Library
# Team


