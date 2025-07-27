from django.http import JsonResponse
from time import time

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

            # Remove entries older than 60 seconds
            self.requests[ip] = [t for t in self.requests[ip] if current_time - t < 60]

            if len(self.requests[ip]) >= 5:
                return JsonResponse({'error': 'Rate limit exceeded. Only 5 messages per minute allowed.'}, status=429)

            self.requests[ip].append(current_time)

        return self.get_response(request)

    def get_client_ip(self, request):
        return request.META.get('REMOTE_ADDR')
