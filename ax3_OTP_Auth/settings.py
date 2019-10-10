from django.conf import settings


OTP_AUTH_PARAMS = getattr(settings, 'OTP_AUTH_PARAMS', [])
OTP_AUTH_TTL = getattr(settings, 'OTP_AUTH_TTL', 60 * 60 * 5)
OTP_AUTH_MESSAGE = getattr(
    settings, 'OTP_AUTH_MESSAGE', 'Utiliza {} como código de inicio de sesión.'
)
OTP_AUTH_COUNTRIES_CODES = getattr(settings, 'OTP_AUTH_COUNTRIES_CODES', [])

AWS_ACCESS_KEY_ID = getattr(settings, 'OTP_AUTH_AWS_ACCESS_KEY_ID', '')
AWS_SECRET_ACCESS_KEY = getattr(settings, 'OTP_AUTH_AWS_SECRET_ACCESS_KEY', '')
AWS_DEFAULT_REGION = getattr(settings, 'OTP_AUTH_AWS_DEFAULT_REGION', 'us-east-1')
