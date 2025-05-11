from rest_framework import routers

from core.viewset.refresh_token import RefreshTokenViewSet

router = routers.SimpleRouter(trailing_slash=False)
router.register(r"", RefreshTokenViewSet, basename="refresh-token")

urlpatterns = router.urls
