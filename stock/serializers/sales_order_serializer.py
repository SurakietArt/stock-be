from typing import Any, Dict

from rest_framework import serializers

from stock.models.sales_order import SaleOrderItem, SalesOrder


class SalesOrderSerializer(serializers.ModelSerializer):
    sale_order = serializers.SerializerMethodField("_get_sale_order_item")

    class Meta:
        model = SalesOrder
        fields = "__all__"

    def _get_sale_order_item(self, obj: SalesOrder) -> Dict[str, Any]:
        order_items = SaleOrderItem.objects.filter(sale_order=obj)
        return SaleOrderItemSerializer(order_items, many=True).data


class SaleOrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = SaleOrderItem
        fields = "__all__"
