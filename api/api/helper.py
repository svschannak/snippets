from api.models import Settings


def get_user_from_request(request):
    print Settings.objects.all().values()
    return Settings.objects.get(token=request.GET['token']).user