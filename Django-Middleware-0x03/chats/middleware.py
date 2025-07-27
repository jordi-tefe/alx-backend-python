# chats/middleware.py

import logging
from django.http import JsonResponse
from time import time


# ---------------------- Request Logging Middleware ----------------------
logger = logging.getLogger(__name__)
handler = logging.FileHandler('requests.log')
formatter = logging.Formatter('%(asctime)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        logger.info(f"{request.method} {request.path}")
        response = self.get_response(request)
        return response


# ---------------------- Throttling Middleware ----------------------
class ThrottlingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.requests = {}  # Tracks IP addresses and timestamps

    def __call__(self, request):
        ip = self.get_client_ip(request)
        current_time = time()

        if request.method == 'POST':
            if ip not in self.requests:
                self.requests[ip] = []

            # Keep only requests from the past 60 seconds
            self.requests[ip] = [t for t in self.requests[ip] if current_time - t < 60]

            if len(self.requests[ip]) >= 5:
                return JsonResponse(
                    {'error': 'Rate limit exceeded. Only 5 messages per minute allowed.'},
                    status=429
                )

            self.requests[ip].append(current_time)

        return self.get_response(request)

    def get_client_ip(self, request):
        # Support for proxies (e.g. Heroku, nginx)
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0]
        return request.META.get('REMOTE_ADDR')
