from rest_framework import serializers

from stock.models.items_model import Items
from stock.serializers.category_serializer import CategorySerializer
from stock.serializers.units_serializer import UnitsSerializer


class ItemsSerializer(serializers.ModelSerializer):
    unit = UnitsSerializer(read_only=True)
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Items
        fields = "__all__"
