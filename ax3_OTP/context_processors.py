from django.conf import settings


def config(request):
    return {
        'REGISTER_WITH_AX3': settings.REGISTER_WITH_AX3,
    }
