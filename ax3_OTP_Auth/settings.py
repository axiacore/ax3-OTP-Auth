from django.conf import settings


OTP_AUTH_PARAMS = getattr(settings, 'OTP_AUTH_PARAMS', [])
OTP_AUTH_TTL = getattr(settings, 'OTP_AUTH_TTL', 60 * 60 * 5)
OTP_AUTH_MESSAGE = getattr(
    settings, 'OTP_AUTH_MESSAGE', 'Utiliza {} como código de inicio de sesión.'
)
OTP_AUTH_COUNTRIES_CODES = getattr(settings, 'OTP_AUTH_COUNTRIES_CODES', [])
OTP_PRIMARY_COLOR = getattr(settings, 'OTP_PRIMARY_COLOR', '#002aff')
OTP_BACKGROUND_BTN = getattr(settings, 'OTP_BACKGROUND_BTN', '#002aff')
OTP_BACKGROUND_BTN_HOVER = getattr(settings, 'OTP_BACKGROUND_BTN_HOVER', '#ff7919')
OTP_COLOR_TEXT_BTN = getattr(settings, 'OTP_COLOR_TEXT_BTN', '#fff')
OTP_COLOR_TEXT_BTN_HOVER = getattr(settings, 'OTP_COLOR_TEXT_BTN_HOVER', '#fff')
OTP_BRAND_NAME = getattr(settings, 'OTP_BRAND_NAME', 'Axiacore')
OTP_BRAND_IMG = getattr(settings, 'OTP_BRAND_IMG', 'otp_auth/img/axiacore-logo.png')
OTP_CUSTOM_SMS_GATEWAY = getattr(settings, 'OTP_CUSTOM_SMS_GATEWAY', None)


AWS_ACCESS_KEY_ID = getattr(settings, 'OTP_AUTH_AWS_ACCESS_KEY_ID', '')
AWS_SECRET_ACCESS_KEY = getattr(settings, 'OTP_AUTH_AWS_SECRET_ACCESS_KEY', '')
AWS_DEFAULT_REGION = getattr(settings, 'OTP_AUTH_AWS_DEFAULT_REGION', 'us-east-1')

LOGIN_URL = getattr(settings, 'LOGIN_URL')
