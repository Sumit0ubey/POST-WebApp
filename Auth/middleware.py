from django.shortcuts import redirect
from django.urls import reverse


class TokenAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.exempt_names = ['Login', 'SignUp', 'Posts', 'Home', 'Contact']

    def __call__(self, request):
        exempt_paths = [reverse(name) for name in self.exempt_names]
        path = request.path

        if path not in exempt_paths and not request.session.get('auth_token'):
            return redirect('Login')

        return self.get_response(request)
