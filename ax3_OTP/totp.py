import pyotp


class AX3TOTP:
    def __init__(self, mobile_phone: int, secret: str):
        self._mobile_phone = mobile_phone
        self._secret = secret

    def create(self, mobile_phone: int, count) -> int:
        totp = pyotp.TOTP(self._secret, digits=6)
        self._send_sms(sms_code=totp.now())
        return self._mobile_phone

    def verify(self, sms_code: int) -> bool:
        totp = pyotp.TOTP(self._secret, digits=6)
        return totp.verify(sms_code)

    def _send_sms(self, sms_code: int):
        print(f'{self._mobile_phone}: {sms_code}')
