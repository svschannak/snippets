from rest_framework.views import APIView
from rest_framework.response import Response
from api.api.helper import get_user_from_request
from api.models import Snippet, SnippetHistory
from guardian.shortcuts import assign_perm
from guardian.shortcuts import get_objects_for_user


class SnippetView(APIView):

    def get(self, request, format=None):
        user = get_user_from_request(request)
        snippets = get_objects_for_user(user, 'api.view_snippet').values('pk', 'name', 'content', 'language', 'created_by__username', 'created_at', 'updated_at')

        return Response({'results': snippets})

    def post(self, request, format=None):

        """
        Creates a new snippet for the user
        """

        user = get_user_from_request(request)

        new_snippet = Snippet.objects.create(name=request.POST['name'], created_by=user, updated_by=user,
                               content=request.POST['content'], language=request.POST['language'])

        assign_perm('view_snippet', user, new_snippet)

        return Response(new_snippet.id)

    def put(self, request):

        user = get_user_from_request(request)

        update_snippet = Snippet.objects.get(id=request.POST['snippet_id'])
        if user.has_perm('view_snippet', update_snippet):

            SnippetHistory.objects.create(origin=update_snippet, name=update_snippet.name, created_by=update_snippet.created_by,
                                   content=update_snippet.content, language=update_snippet.language)

            update_snippet.name = request.POST['name']
            update_snippet.content = request.POST['content']
            update_snippet.language = request.POST['language']
            update_snippet.save()

            return Response(update_snippet.id)
        else:
            return Response('No rights to do this.')