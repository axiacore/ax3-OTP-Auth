from django.contrib.auth.backends import ModelBackend, UserModel


class OTPAuthBackend(ModelBackend):
    # pylint: disable=arguments-differ
    def authenticate(self, request, mobile_phone=None):
        try:
            user = UserModel.objects.get(mobile_phone=mobile_phone)
        except (UserModel.DoesNotExist, UserModel.MultipleObjectsReturned):
            return None
        else:
            if self.user_can_authenticate(user):
                return user
        return None
