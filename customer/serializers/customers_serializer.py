from rest_framework import serializers

from customer.models.customers_model import Customers


class CustomersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customers
        fields = "__all__"
