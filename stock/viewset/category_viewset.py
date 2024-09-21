from rest_framework import viewsets

from stock.models.category_model import Category
from stock.serializers.category_serializer import CategorySerializer


class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
