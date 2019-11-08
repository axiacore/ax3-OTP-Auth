from django.conf import settings


OTP_AUTH_PARAMS = getattr(settings, 'OTP_AUTH_PARAMS', [])
OTP_AUTH_TTL = getattr(settings, 'OTP_AUTH_TTL', 60 * 60 * 5)
OTP_AUTH_MESSAGE = getattr(
    settings, 'OTP_AUTH_MESSAGE', 'Utiliza {} como código de inicio de sesión.'
)
OTP_AUTH_COUNTRIES_CODES = getattr(settings, 'OTP_AUTH_COUNTRIES_CODES', [])

OTP_PRIMARY_COLOR = getattr(settings, 'OTP_PRIMARY_COLOR', '#002aff')
OTP_SECONDARY_COLOR = getattr(settings, 'OTP_SECONDARY_COLOR', '#f3f9ff')
OTP_BRAND_NAME = getattr(settings, 'OTP_BRAND_NAME', 'Axiacore')

AWS_ACCESS_KEY_ID = getattr(settings, 'OTP_AUTH_AWS_ACCESS_KEY_ID', '')
AWS_SECRET_ACCESS_KEY = getattr(settings, 'OTP_AUTH_AWS_SECRET_ACCESS_KEY', '')
AWS_DEFAULT_REGION = getattr(settings, 'OTP_AUTH_AWS_DEFAULT_REGION', 'us-east-1')

