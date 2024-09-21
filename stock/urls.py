from rest_framework import routers

from stock.viewset.items_viewset import ItemsViewSet

router = routers.SimpleRouter(trailing_slash=False)
router.register(r"items", ItemsViewSet, basename="items")

urlpatterns = router.urls
