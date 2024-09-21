from rest_framework import viewsets

from stock.models.items_model import Items
from stock.serializers.items_serializer import ItemsSerializer


class ItemsViewSet(viewsets.ModelViewSet):
    serializer_class = ItemsSerializer
    queryset = Items.objects.all()
