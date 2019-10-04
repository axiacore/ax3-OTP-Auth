from urllib import parse

from django.views.generic import FormView, TemplateView
from django.urls import reverse
from django.shortcuts import redirect

from .hotp import HOTP
from .settings import PARAMS
from .forms import SMSForm, OTPForm


class SMSView(FormView):
    template_name = 'ax3/sms.html'
    form_class = SMSForm

    def form_valid(self, form):
        hotp = HOTP(session_key=self.request.session.session_key)
        hotp.create(
            country_code=form.cleaned_data['country_code'],
            phone_number=form.cleaned_data['phone_number']
        )

        params = {
            'country_code': form.cleaned_data['country_code'],
            'phone_number': form.cleaned_data['phone_number'],
            'redirect': self.request.GET['redirect'],
        }
        if PARAMS:
            for param in PARAMS:
                params[param] = self.request.GET.get(param)

        return redirect('{}?{}'.format(reverse('ax3:otp'), parse.urlencode(params, safe='/')))


class OTPView(FormView):
    template_name = 'ax3/otp.html'
    form_class = OTPForm

    def get_initial(self):
        initial = super().get_initial()
        initial.update({
            'country_code': self.request.GET.get('country_code'),
            'phone_number': self.request.GET.get('phone_number'),
        })
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        params = {'redirect': self.request.GET['redirect']}
        if PARAMS:
            for param in PARAMS:
                params[param] = self.request.GET.get(param)
        context['sms_url'] = '{}?{}'.format(reverse('ax3:sms'), parse.urlencode(params, safe='/'))
        return context

    def form_valid(self, form):
        cleaned_data = form.cleaned_data
        hotp = HOTP(session_key=self.request.session.session_key)

        token = hotp.verify(cleaned_data.get('code', ''), phone_number=cleaned_data['phone_number'])
        if not token:
            form.add_error('code', 'Código no es valido')
            return self.form_invalid(form)

        params = {'token': token, 'redirect': self.request.GET['redirect']}
        if PARAMS:
            for param in PARAMS:
                params[param] = self.request.GET.get(param)

        return redirect('{}?{}'.format(reverse('ax3:done'), parse.urlencode(params, safe='/')))


class DoneView(TemplateView):
    template_name = 'ax3/done.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        params = {'token': self.request.GET['token']}
        if PARAMS:
            for param in PARAMS:
                params[param] = self.request.GET.get(param)

        context['redirect'] = '{}?{}'.format(
            self.request.GET['redirect'],
            parse.urlencode(params, safe='/')
        )
        return context
