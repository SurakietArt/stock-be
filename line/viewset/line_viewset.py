import uuid
from urllib.parse import urlencode

from django.conf import settings
from django.contrib.auth import login
from django.contrib.auth import get_user_model
from django.shortcuts import redirect
from rest_framework import status, viewsets
from rest_framework.decorators import action, renderer_classes
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework_simplejwt.tokens import RefreshToken

from line.services.line_services import LineService

User = get_user_model()


class LineViewSet(GenericViewSet):

    @action(detail=False, methods=["get"], url_path="login", url_name="login")
    def line_login(self, request: Request) -> Response:
        state = str(uuid.uuid4())
        request.session['line_login_state'] = state
        login_url = settings.LINE_LOGIN_URL.format(
            client_id=settings.LINE_LOGIN_CLIENT_ID,
            redirect_uri=settings.LINE_LOGIN_REDIRECT_URI,
            state=state
        )
        return redirect(login_url)

    @action(detail=False, methods=["get"], url_path="callback", url_name="callback")
    def line_callback(self, request: Request) -> Response:
        code = request.GET.get("code")
        state = request.GET.get("state")

        if not code or state != request.session.get("line_login_state"):
            return Response(data="Invalid request", status=status.HTTP_400_BAD_REQUEST)
        line_access_token = LineService.get_access_from_code(code)
        user = LineService.get_user_from_access_token(line_access_token)
        login(request, user)
        refresh = RefreshToken.for_user(user)
        params = urlencode({
            "access": str(refresh.access_token),
            "refresh": str(refresh),
            "name": user.first_name,
        })

        return redirect(f"{settings.FRONTEND_REDIRECT_URL}?{params}")


@renderer_classes([TemplateHTMLRenderer])
class LineTemplateViewSet(viewsets.GenericViewSet):

    @action(detail=False, methods=["get"], url_path="callback", url_name="callback")
    def line_call_back(self, request):
        return Response(template_name="line_callback.html")

