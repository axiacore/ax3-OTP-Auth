from django.conf import settings


def global_settings(request):
    return {
        'OTP_PRIMARY_COLOR': settings.OTP_PRIMARY_COLOR,
        'OTP_BACKGROUND_BTN': settings.OTP_BACKGROUND_BTN,
        'OTP_BACKGROUND_BTN_HOVER': settings.OTP_BACKGROUND_BTN_HOVER,
        'OTP_COLOR_TEXT_BTN': settings.OTP_COLOR_TEXT_BTN,
        'OTP_COLOR_TEXT_BTN_HOVER': settings.OTP_COLOR_TEXT_BTN_HOVER,
        'OTP_BRAND_NAME': settings.OTP_BRAND_NAME,
        'OTP_BRAND_IMG': settings.OTP_BRAND_IMG,
    }
