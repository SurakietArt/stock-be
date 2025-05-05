from rest_framework import serializers

from core.serializer.base_serializer import BaseSerializer
from stock.models.items_model import Items
from stock.serializers.category_serializer import CategoryPartialSerializer
from stock.serializers.units_serializer import UnitsPartialSerializer


class ItemsSerializer(BaseSerializer):
    unit = UnitsPartialSerializer(read_only=True)
    category = CategoryPartialSerializer(read_only=True)
    unit_id = serializers.IntegerField(write_only=True)
    category_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Items
        exclude = ["barcode", "deleted", "deleted_by_cascade"]
