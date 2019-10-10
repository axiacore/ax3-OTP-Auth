from django.urls import path

from . import views


app_name = 'ax3_otp_auth'
urlpatterns = [
    path(
        'start/',
        views.StartView.as_view(),
        name='start',
    ),

    path(
        'verify/',
        views.VerifyView.as_view(),
        name='verify',
    ),

    path(
        'done/',
        views.DoneView.as_view(),
        name='done',
    ),
]
