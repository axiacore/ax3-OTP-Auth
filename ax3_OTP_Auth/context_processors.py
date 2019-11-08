from django.conf import settings

def global_settings(request):
    return {
        'OTP_PRIMARY_COLOR': settings.OTP_PRIMARY_COLOR,
        'OTP_SECONDARY_COLOR': settings.OTP_SECONDARY_COLOR,
        'OTP_BRAND_NAME': settings.OTP_BRAND_NAME,
    }
