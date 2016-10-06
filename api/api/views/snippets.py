from rest_framework.views import APIView
from rest_framework.response import Response
from api.api.helper import get_user_from_request
from api.models import Snippet, SnippetHistory

from guardian.shortcuts import assign_perm
from guardian.shortcuts import get_objects_for_user

from api.api.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated


class SnippetView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request, format=None):

        snippets = get_objects_for_user(request.user, 'api.view_snippet').values('pk', 'name', 'content', 'language', 'created_by__username', 'created_at', 'updated_at')

        if hasattr(request.data, 'snippet_id'):
            snippets = snippets.filter(id=request.data['snippet_id'])

        return Response({'results': snippets})

    def post(self, request, format=None):

        """
        Creates a new snippet for the user
        """

        new_snippet = Snippet.objects.create(name=request.data['name'], created_by=request.user, updated_by=request.user,
                               content=request.data['content'], language=request.data['language'])

        assign_perm('view_snippet', request.user, new_snippet)

        return Response(new_snippet.id)

    def put(self, request):

        update_snippet = Snippet.objects.get(id=request.data['snippet_id'])
        if request.user.has_perm('view_snippet', update_snippet):

            SnippetHistory.objects.create(origin=update_snippet, name=update_snippet.name, created_by=update_snippet.created_by,
                                   content=update_snippet.content, language=update_snippet.language)

            update_snippet.name = request.data['name']
            update_snippet.content = request.data['content']
            update_snippet.language = request.data['language']
            update_snippet.save()

            return Response(update_snippet.id)
        else:
            return Response('No rights to do this.')

    def delete(self, request):
        remove_snippet = Snippet.objects.get(id=request.data['snippet_id'])
        if request.user.has_perm('view_snippet', remove_snippet):
            remove_snippet.delete()

        return Response('Deleted')