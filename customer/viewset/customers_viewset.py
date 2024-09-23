from rest_framework import viewsets

from customer.models.customers_model import Customers
from customer.serializers.customers_serializer import CustomersSerializer


class CustomersViewSet(viewsets.ModelViewSet):
    serializer_class = CustomersSerializer
    queryset = Customers.objects.all()
