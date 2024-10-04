from rest_framework import serializers

from customer.serializers.customers_serializer import CustomersSerializer
from stock.models.invoice import Invoice
from stock.serializers.sales_order_serializer import SalesOrderSerializer


class InvoiceSerializer(serializers.ModelSerializer):
    customer = CustomersSerializer()
    sales_order = SalesOrderSerializer()

    class Meta:
        model = Invoice
        fields = "__all__"
