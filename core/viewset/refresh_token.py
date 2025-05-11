from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import GenericViewSet
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from rest_framework.exceptions import AuthenticationFailed


class RefreshTokenViewSet(GenericViewSet):
    authentication_classes = []
    permission_classes = []

    @action(detail=False, methods=["post"], url_path="refresh", url_name="refresh")
    def post(self, request):
        refresh_token = request.COOKIES.get('refresh_token')

        if not refresh_token:
            raise AuthenticationFailed("Refresh token not found in cookie")

        try:
            refresh = RefreshToken(refresh_token)
            access_token = str(refresh.access_token)
            return Response({
                "access": access_token
            }, status=status.HTTP_200_OK)
        except TokenError as e:
            raise AuthenticationFailed(f"Invalid refresh token: {e}")
