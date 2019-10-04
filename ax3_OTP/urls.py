from django.urls import path

from . import views


app_name = 'ax3_otp'
urlpatterns = [
    path(
        'ingresar/',
        views.SMSView.as_view(),
        name='sms',
    ),

    path(
        'ingresar/password/',
        views.OTPView.as_view(),
        name='otp',
    ),

    path(
        'ingresar/hecho/',
        views.DoneView.as_view(),
        name='done',
    ),
]
