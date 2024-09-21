from rest_framework import viewsets

from stock.models.units_model import Units
from stock.serializers.units_serializer import UnitsSerializer


class UnitsViewSet(viewsets.ModelViewSet):
    serializer_class = UnitsSerializer
    queryset = Units.objects.all()
