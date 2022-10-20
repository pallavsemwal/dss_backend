from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from django.http import HttpResponseForbidden


class JWTMiddleware(object):

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        if request.META.get('PATH_INFO') == '/graphql':
            token = request.META.get('HTTP_AUTHORIZATION', '')
            if not token.startswith('JWT'):
                return HttpResponseForbidden('Access Denied')
            jwt_auth = JSONWebTokenAuthentication()
            auth = None
            try:
                auth = jwt_auth.authenticate(request)
            except Exception:
                return HttpResponseForbidden('Access Denied')
            request.user = auth[0]