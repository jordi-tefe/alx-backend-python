# chats/middleware.py

import logging
from django.http import JsonResponse
from time import time
import gzip
from io import BytesIO
from django.utils.deprecation import MiddlewareMixin

# ---------------------- Request Logging Middleware ----------------------
logger = logging.getLogger(__name__)
handler = logging.FileHandler('requests.log')
formatter = logging.Formatter('%(asctime)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        current_time = datetime.now().time()
        start = datetime.strptime("09:00", "%H:%M").time()
        end = datetime.strptime("17:00", "%H:%M").time()

        if not (start <= current_time <= end):
            return JsonResponse(
                {"error": "Access restricted to working hours (9AM–5PM)."},
                status=403
            )

        return self.get_response(request)

# Task 3: Rate-limiting offensive language
class OffensiveLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.requests = {}

    def __call__(self, request):
        ip = self.get_client_ip(request)
        current_time = time()

        if request.method == 'POST':
            if ip not in self.requests:
                self.requests[ip] = []

            # Remove timestamps older than 60 seconds
            self.requests[ip] = [t for t in self.requests[ip] if current_time - t < 60]

            if len(self.requests[ip]) >= 5:
                return JsonResponse({'error': 'Rate limit exceeded. Only 5 messages per minute allowed.'}, status=429)

            self.requests[ip].append(current_time)

        return self.get_response(request)

    def get_client_ip(self, request):
        return request.META.get('REMOTE_ADDR')


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

class GzipMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        # Check if the client accepts gzip
        if 'gzip' not in request.META.get('HTTP_ACCEPT_ENCODING', ''):
            return response

        # Skip compression for already compressed responses
        if response.has_header('Content-Encoding'):
            return response

        # Only compress for HTTP 200 OK and content with a body
        if response.status_code != 200 or not response.content:
            return response

        # Compress the response
        gzip_buffer = BytesIO()
        with gzip.GzipFile(mode='wb', fileobj=gzip_buffer) as gzip_file:
            gzip_file.write(response.content)

        # Set new response content
        response.content = gzip_buffer.getvalue()
        response['Content-Encoding'] = 'gzip'
        response['Content-Length'] = str(len(response.content))

        return response

class RolepermissionMiddleware(MiddlewareMixin):
    def process_view(self, request, view_func, view_args, view_kwargs):
        if request.path.startswith('/messages/'):
            role = request.META.get('HTTP_ROLE')
            if role != 'admin':
                return JsonResponse({'error': 'Access denied: Admins only'}, status=403)
        return None
