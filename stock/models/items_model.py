from django.db import models

from core.models.base_model import BaseModel
from stock.models.category_model import Category
from stock.models.units_model import Units


class Items(BaseModel):
    name = models.CharField(max_length=255)
    barcode = models.CharField(max_length=255, db_index=True, unique=True)
    sku = models.CharField(max_length=255, db_index=True, unique=True)
    amount = models.IntegerField()
    price_per_unit = models.FloatField()
    unit = models.ForeignKey(
        Units, on_delete=models.SET_NULL, related_name="item_unit", null=True
    )
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, related_name="item_category", null=True
    )
    alert_threshold = models.IntegerField(null=True, blank=True)

    class Meta:
        ordering = ['id']
