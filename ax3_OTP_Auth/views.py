from urllib import parse
from secrets import token_urlsafe

from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import FormView, TemplateView

from .forms import StartForm, VerifyForm
from .hotp import HOTP
from .settings import OTP_AUTH_PARAMS, LOGIN_URL


class StartView(FormView):
    template_name = 'otp_auth/start.html'
    form_class = StartForm

    def render_to_response(self, context, **response_kwargs):
        response = super().render_to_response(context, **response_kwargs)
        if not self.request.COOKIES.get('otp_unique_id', None):
            response.set_cookie('otp_unique_id', token_urlsafe())
        return response

    def form_valid(self, form):
        unique_id = self.request.COOKIES.get('otp_unique_id', None)
        if not unique_id:
            return redirect('otp_auth:start')

        hotp = HOTP(unique_id=unique_id)
        hotp.create(
            country_code=form.cleaned_data['country_code'],
            phone_number=form.cleaned_data['phone_number']
        )

        params = {
            'country_code': form.cleaned_data['country_code'],
            'phone_number': form.cleaned_data['phone_number'],
            'redirect': self.request.GET.get('redirect', reverse(LOGIN_URL)),
        }
        if OTP_AUTH_PARAMS:
            for param in OTP_AUTH_PARAMS:
                params[param] = self.request.GET.get(param)

        return redirect('{}?{}'.format(
            reverse('otp_auth:verify'),
            parse.urlencode(params, safe='/'))
        )


class VerifyView(FormView):
    template_name = 'otp_auth/verify.html'
    form_class = VerifyForm

    def get_initial(self):
        initial = super().get_initial()
        initial.update({
            'country_code': self.request.GET.get('country_code'),
            'phone_number': self.request.GET.get('phone_number'),
        })
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        params = {'redirect': self.request.GET.get('redirect', reverse(LOGIN_URL))}
        if OTP_AUTH_PARAMS:
            for param in OTP_AUTH_PARAMS:
                params[param] = self.request.GET.get(param)
        context['sms_url'] = '{}?{}'.format(
            reverse('otp_auth:start'),
            parse.urlencode(params, safe='/')
        )
        return context

    def form_valid(self, form):
        cleaned_data = form.cleaned_data

        hotp = HOTP(unique_id=self.request.COOKIES.get('otp_unique_id', ''))

        token = hotp.verify(cleaned_data.get('code', ''), phone_number=cleaned_data['phone_number'])
        if not token:
            form.add_error('code', 'Código no es valido')
            return self.form_invalid(form)

        params = {'token': token, 'redirect': self.request.GET.get('redirect', reverse(LOGIN_URL))}
        if OTP_AUTH_PARAMS:
            for param in OTP_AUTH_PARAMS:
                params[param] = self.request.GET.get(param)

        return redirect('{}?{}'.format(reverse('otp_auth:done'), parse.urlencode(params, safe='/')))


class DoneView(TemplateView):
    template_name = 'otp_auth/done.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        params = {'token': self.request.GET['token']}
        if OTP_AUTH_PARAMS:
            for param in OTP_AUTH_PARAMS:
                params[param] = self.request.GET.get(param)

        context['redirect'] = '{}?{}'.format(
            self.request.GET.get('redirect', reverse(LOGIN_URL)),,
            parse.urlencode(params, safe='/')
        )
        return context
