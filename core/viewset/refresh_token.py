import uuid

from django.conf import settings
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import GenericViewSet
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from rest_framework.exceptions import AuthenticationFailed

from line.viewset.line_viewset import LineViewSet


class RefreshTokenViewSet(GenericViewSet):
    authentication_classes = []
    permission_classes = []

    @action(detail=False, methods=["post"], url_path="refresh", url_name="refresh")
    def post(self, request):
        refresh_token = request.COOKIES.get('refresh_token')

        if not refresh_token:
            state = str(uuid.uuid4())
            request.session['line_login_state'] = state
            login_url = settings.LINE_LOGIN_URL.format(
                client_id=settings.LINE_LOGIN_CLIENT_ID,
                redirect_uri=settings.LINE_LOGIN_REDIRECT_URI,
                state=state
            )
            return Response({
                "detail": "Missing refresh token",
                "login_url": login_url
            }, status=status.HTTP_401_UNAUTHORIZED)

        try:
            refresh = RefreshToken(refresh_token)
            access_token = str(refresh.access_token)
            return Response({
                "access": access_token
            }, status=status.HTTP_200_OK)
        except TokenError as e:
            raise AuthenticationFailed(f"Invalid refresh token: {e}")
