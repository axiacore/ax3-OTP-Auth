from django import forms
from django.core.validators import MinLengthValidator, RegexValidator

from .data import CONTRY_CODE_CHOICES


class SMSForm(forms.Form):
    country_code = forms.ChoiceField(
        choices=CONTRY_CODE_CHOICES,
    )

    phone_number = forms.CharField(
        max_length=25,
        validators=[
            RegexValidator(r'^[0-9]*$', message='Ingresa solo números'),
            MinLengthValidator(10),
        ]
    )


class OTPForm(SMSForm, forms.Form):
    HIDDEN_FIELDS = ['country_code', 'phone_number']

    code = forms.CharField(
        max_length=6,
        validators=[
            RegexValidator(r'^[0-9]*$', message='Ingresa solo números'),
            MinLengthValidator(6),
        ]
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.HIDDEN_FIELDS:
            self.fields[field].widget = forms.HiddenInput()
