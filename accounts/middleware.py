from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse

class AdminOnlyMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        admin_paths = ['/admin/', '/cms/']

        if any(request.path.startswith(path) for path in admin_paths):
            if not request.user.is_authenticated or not request.user.is_superuser:
                return render(request, 'pages/forbidden.html', status=403)

        return self.get_response(request)
