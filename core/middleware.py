from django.utils.deprecation import MiddlewareMixin


class DeveloperMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        response.headers["X-Developer"] = "gledi"
        return response
