class AX3OTPMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if 'ax3_otp' not in request.session:
            request.session['ax3_otp'] = True
            request.session.save()

        response = self.get_response(request)
        return response
