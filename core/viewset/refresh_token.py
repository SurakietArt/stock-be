from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import GenericViewSet
from rest_framework_simplejwt.tokens import RefreshToken, TokenError

from line.services.line_services import LineService


class RefreshTokenViewSet(GenericViewSet):
    authentication_classes = []
    permission_classes = []

    @action(detail=False, methods=["post"], url_path="refresh", url_name="refresh")
    def post(self, request: Request):
        refresh_token = request.COOKIES.get('refresh_token')

        if not refresh_token:
            return Response({
                "detail": "Missing refresh token",
                "login_url": LineService.create_login_url(request)
            }, status=status.HTTP_401_UNAUTHORIZED)

        try:
            refresh = RefreshToken(refresh_token)
            access_token = str(refresh.access_token)
            return Response({
                "access": access_token
            }, status=status.HTTP_200_OK)
        except TokenError:
            return Response({
                "detail": "Refresh token expire",
                "login_url": LineService.create_login_url(request)
            }, status=status.HTTP_401_UNAUTHORIZED)
