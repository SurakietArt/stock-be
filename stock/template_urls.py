from rest_framework import routers

from stock.viewset.items_viewset import ItemTemplateViewSet

router = routers.SimpleRouter(trailing_slash=False)
router.register(r"", ItemTemplateViewSet, basename="items-template")

urlpatterns = router.urls
