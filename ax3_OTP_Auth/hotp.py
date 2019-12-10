from secrets import token_urlsafe

from django.core.cache import cache
from django.utils.module_loading import import_string

import boto3
import pyotp

from . import settings


class HOTP:
    def __init__(self, unique_id: str, digits: int = 6):
        self._unique_id = unique_id
        self._digits = digits
        self._ttl = settings.OTP_AUTH_TTL

    def _create_secret(self, secret: str) -> str:
        cache.set('{}.secret'.format(self._unique_id), secret, timeout=self._ttl)
        return secret

    def _create_counter(self) -> str:
        try:
            cache.incr('{}.counter'.format(self._unique_id))
        except ValueError:
            cache.set('{}.counter'.format(self._unique_id), 1, timeout=self._ttl)
        return cache.get('{}.counter'.format(self._unique_id))

    def _create_token(self, phone_number: int) -> str:
        token = token_urlsafe()
        cache.set(token, phone_number, timeout=self._ttl)
        return token

    def _get_secret(self):
        return cache.get('{}.secret'.format(self._unique_id))

    def _get_counter(self):
        return cache.get('{}.counter'.format(self._unique_id))

    def _send_sms(self, sms_code: int, country_code: str, phone_number: int):
        message = settings.OTP_AUTH_MESSAGE.format(sms_code)

        if settings.OTP_CUSTOM_SMS_GATEWAY:
            gateway = import_string(settings.OTP_CUSTOM_SMS_GATEWAY)
            gateway(country_code=country_code, phone_number=phone_number, message=message)

        else:
            sns = boto3.client(
                'sns',
                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                region_name=settings.AWS_DEFAULT_REGION
            )

            sns.publish(
                PhoneNumber=f'+{country_code}{phone_number}',
                Message=message,
                MessageAttributes={
                    'AWS.SNS.SMS.SMSType': {
                        'DataType': 'String',
                        'StringValue': 'Transactional'
                    }
                }
            )

    def create(self, country_code: str, phone_number: int):
        secret = self._create_secret(secret=pyotp.random_base32(length=32))
        counter = self._create_counter()

        hotp = pyotp.HOTP(secret, digits=self._digits)
        self._send_sms(
            sms_code=hotp.at(counter),
            country_code=country_code,
            phone_number=phone_number
        )

    def verify(self, sms_code: int, phone_number: int) -> str:
        secret = self._get_secret()
        count = self._get_counter()

        if count and secret:
            hotp = pyotp.HOTP(secret, digits=self._digits)
            if hotp.verify(sms_code, count):
                return self._create_token(phone_number=phone_number)
        return None

    def get_phone_number(self, token: str) -> int:
        phone_number = cache.get(token)
        cache.delete(token)
        cache.delete_pattern('{}.*'.format(self._unique_id))
        return phone_number
