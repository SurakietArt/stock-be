from rest_framework import routers

from customer.viewset.customers_viewset import CustomersViewSet

router = routers.SimpleRouter(trailing_slash=False)
router.register(r"", CustomersViewSet, basename="customers")

urlpatterns = router.urls
