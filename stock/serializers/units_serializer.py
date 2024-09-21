from rest_framework import serializers

from stock.models.units_model import Units


class UnitsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Units
        fields = "__all__"
