# AX3 OTP

AX3 OTP is a very simple Django library for generating and verifying one-time passwords using HTOP guidelines.

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
        'ax3_OTP',
    ]

**2.** Add ``ax3_OTP.backends.AX3OTPBackend`` to the top of ``AUTHENTICATION_BACKENDS``:

    AUTHENTICATION_BACKENDS = [
        'ax3_OTP.backends.AX3OTPBackend',

        # Django ModelBackend is the default authentication backend.
        'django.contrib.auth.backends.ModelBackend',
    ]

**3.** Add ``ax3_OTP.middleware.AX3OTPMiddleware`` to your list of ``MIDDLEWARE``:

    MIDDLEWARE = [
        # The following is the list of default middleware in new Django projects.
        'django.middleware.security.SecurityMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',

        'ax3_OTP.middleware.AX3OTPMiddleware',
    ]

**4.** Add ``ax3_OTP.context_processor.config`` to your list of ``OPTIONS``:

    'context_processors' = [
        # The following is the list of default context processor in new Django projects.
        'django.template.context_processors.debug',
        'django.contrib.auth.context_processors.auth',
        'django.contrib.messages.context_processors.messages',
        'django.template.context_processors.request',

        'ax3_OTP.context_processor.config',
    ]

**5.** Add the following to your urls.py:

    urlpatterns = [
        path('ax3/', include('ax3_OTP.urls', namespace='ax3')),
    ]

**6.** Create html button to your template:

    <button class="js-ax3-sms-login" type="button" ax3-login="{% url 'ax3:sms' %}" ax3-redirect="{% url 'login' %}">
        Login
    </button>

**7.** Create Javascript for open OTP window:

    $(() => {
        $('.js-ax3-sms-login').on('click', function() {
            let redirect = $(this).attr('ax3-redirect');
            let ax3LoginUrl = $(this).attr('ax3-login');

            window.open(`${window.origin}${ax3LoginUrl}?redirect=${redirect}`, '_blank', 'location=yes,height=470,width=420,scrollbars=yes,status=yes');
        });
    });

## Configuration

If your need pass any param for whole pipeline you can use `AX3_OTP_PARAMS`:

    `AX3_OTP_PARAMS = ['param']`

If your need change life time cache value you can use `AX3_OTP_LIFE_TIME`:

    `AX3_OTP_LIFE_TIME = 60 * 60 * 5  # 5 minutes`

If your need change sms message:

    `AX3_OTP_MESSAGE = 'Utiliza {} como código de inicio de sesión.`

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

    AWS_ACCESS_KEY_ID = ''
    AWS_SECRET_ACCESS_KEY = ''
    AWS_DEFAULT_REGION = 'us-west-2'

## Authentication and Authorization

Authenticated user requires an OTP, this OTP was sent by AWS SNS service, once the code is valid, the system returns a token that must then be used to obtain the phone number which was requested. for this purpose you can use 'get_phone_number':

    hotp = HOTP(session_key=request.session.session_key)
    phone_number = htop.get_phone_number(code='123')
