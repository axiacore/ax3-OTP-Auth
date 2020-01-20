# AX3 OTP Auth

AX3 OTP Auth is a very simple Django library for generating and verifying one-time passwords using HTOP guidelines.

## Installation

Axes is easy to install from the PyPI package:

    $ pip install django-axes

After installing the package, the project settings need to be configured.

**1.** Add ``ax3_OTP`` to your ``INSTALLED_APPS``::

    INSTALLED_APPS = [
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',

        # Axes app can be in any position in the INSTALLED_APPS list.
        'ax3_OTP_Auth',
    ]

**2.** Add ``ax3_OTP_Auth.backends.OTPAuthBackend`` to the top of ``AUTHENTICATION_BACKENDS``:

    AUTHENTICATION_BACKENDS = [
        'ax3_OTP_Auth.backends.OTPAuthBackend',

        # Django ModelBackend is the default authentication backend.
        'django.contrib.auth.backends.ModelBackend',
    ]

**3.** Add the following to your urls.py:

    urlpatterns = [
        path('OTP-Auth/', include('ax3_OTP_Auth.urls', namespace='otp_auth')),
    ]

**4.** Create html button to your template:

    <button class="js-otp-auth" type="button" otp-login="{% url 'otp_auth:start' %}" otp-redirect="{% url 'login' %}">
        Login
    </button>

**5.** Create Javascript for open OTP window:

    $(() => {
        $('.js-otp-auth').on('click', function () {
            let redirect = $(this).attr('otp-redirect');
            let OTPLoginUrl = $(this).attr('otp-login');

            let width = 420;
            let height = 470;
            let top = (screen.height / 2) - (height / 2);
            let left = (screen.width / 2) - (width / 2);

            window.open(`${window.origin}${OTPLoginUrl}?redirect=${redirect}`, '_blank', `location=yes, scrollbars=yes, status=yes, width=${width}, height=${height}, top=${top}, left=${left}`);
        });
    });

## Configuration

If your need pass any param for whole pipeline you can use `OTP_AUTH_PARAMS`:

    `OTP_AUTH_PARAMS = ['param']`

If your need change life time cache value you can use `OTP_AUTH_TTL`:

    `OTP_AUTH_TTL = 60 * 60 * 5  # 5 minutes`

If your need change sms message:

    `OTP_AUTH_MESSAGE = 'Utiliza {} como código de inicio de sesión.`

Configure countries allowed list:
    COLOMBIA = 57
    ARGENTINA = 54
    BOLIVIA = 591
    CHILE = 56
    COSTA_RICA = 506
    CUBA = 53
    DOMINICAN_REPUBLIC = 809
    ECUADOR = 593
    GUATEMALA = 502
    MEXICO = 52
    PERU = 51

    OTP_AUTH_COUNTRIES_CODES = [57, 54]

Change color, brand name and logo using this variables:

    OTP_PRIMARY_COLOR = '#eb6806'
    OTP_BACKGROUND_BTN = '#eb6806'
    OTP_BACKGROUND_BTN_HOVER = '#000'
    OTP_COLOR_TEXT_BTN = '#fff'
    OTP_COLOR_TEXT_BTN_HOVER = '#fff'
    OTP_BRAND_NAME = 'Axiacore'
    OTP_BRAND_IMG = 'user-relative-path'


## NSN Configuration

AX3 OTP use NSN AWS service for sending messages, please create a group and AIM user with the following policy:

    {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Action": [
                    "sns:Publish",
                    "sns:SetSMSAttributes",
                    "sns:GetSMSAttributes"
                ],
                "Resource": "*"
            }
        ]
    }

Set AIM user credentials to your settings:

    OTP_AUTH_AWS_ACCESS_KEY_ID = ''
    OTP_AUTH_AWS_SECRET_ACCESS_KEY = ''
    OTP_AUTH_AWS_DEFAULT_REGION = 'us-west-2'

## Authentication and Authorization

Authenticated user requires an OTP, this OTP was sent by AWS SNS service, once the code is valid, the system returns a token that must then be used to obtain the phone number which was requested. for this purpose you can use 'get_phone_number':

    hotp = HOTP(session_key=request.session.session_key)
    phone_number = htop.get_phone_number(code='123')

## Custom SMS Gateway

Set ``OTP_CUSTOM_SMS_GATEWAY`` to your settings with the path of your function and the function must be receive ``country_code``, ``phone_number`` and ``message``

    OTP_CUSTOM_SMS_GATEWAY = 'app.utils.send_sms'

## Style SASS

For development porpuse is necessary to compile the SASS files before you commit any change.

Install node from this link:

    https://nodejs.org/en/

Then install sass

    $ sudo npm install -g sass

It ask you for a password, write de password of the user of the computer.


## Compile SASS

To change the styles of the web page you need to do edit the Sass's files and
then run this command on the root folder of the project to compile it to CSS:

    $ sass --watch ax3_OTP_Auth/static/otp_auth/sass/styles.sass ax3_OTP_Auth/static/otp_auth/css/styles.css
