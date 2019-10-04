from django.conf import settings


PARAMS = getattr(settings, 'AX3_OTP_PARAMS', [])
LIFE_TIME = getattr(settings, 'AX3_OTP_LIFE_TIME', 60 * 60 * 5)
MESSAGE = getattr(settings, 'AX3_OTP_MESSAGE', 'Utiliza {} como código de inicio de sesión.')

AWS_ACCESS_KEY_ID = getattr(settings, 'AWS_ACCESS_KEY_ID', '')
AWS_SECRET_ACCESS_KEY = getattr(settings, 'AWS_SECRET_ACCESS_KEY', '')
AWS_DEFAULT_REGION = getattr(settings, 'AWS_DEFAULT_REGION', '')
