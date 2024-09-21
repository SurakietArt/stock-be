from rest_framework import serializers

from stock.models.category_model import Category
from stock.models.items_model import Items
from stock.models.units_model import Units


class ItemsSerializer(serializers.ModelSerializer):
    unit = serializers.ModelSerializer(Units, read_only=True)
    category = serializers.ModelSerializer(Category, read_only=True)

    class Meta:
        model = Items
        fields = "__all__"
