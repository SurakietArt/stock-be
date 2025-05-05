from rest_framework import serializers

from stock.models.category_model import Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class CategoryPartialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["name"]
