from rest_framework import routers

from stock.viewset.category_viewset import CategoryViewSet
from stock.viewset.items_viewset import ItemsViewSet
from stock.viewset.unit_viewset import UnitsViewSet

router = routers.SimpleRouter(trailing_slash=False)
router.register(r"items", ItemsViewSet, basename="items")
router.register(r"categories", CategoryViewSet, basename="category")
router.register(r"units", UnitsViewSet, basename="units")

urlpatterns = router.urls
