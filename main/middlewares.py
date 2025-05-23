from django.conf import settings
from django.http import JsonResponse


class AuthenticatePublicEndpointMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_view(self, request, view_func, view_args, view_kwargs):
        if self.eligible_endpoint(request):
            api_key = request.META.get("HTTP_API_KEY")

            if not api_key:
                return JsonResponse({
                    "status": False,
                    "message": "'api-key' is missing from request headers."
                }, status=400)

            auth = settings.APP_API_KEY == api_key

            if not auth:
                return JsonResponse({
                    "message": "Unauthorized"
                }, status=401)

        return None

    def eligible_endpoint(self, request):
        if request.path in (
            '/api/data/get-chart-data/',
        ):
            return True

        return False
