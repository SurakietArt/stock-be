from django.db import models

from core.models.base_model import BaseModel
from stock.models.category import Category
from stock.models.units import Units


class Items(BaseModel):
    name = models.CharField(max_length=255)
    amount = models.IntegerField()
    price = models.FloatField()
    price_per_unit = models.FloatField()
    unit = models.ForeignKey(Units, on_delete=models.SET_NULL, related_name="item_unit")
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, related_name="item_category"
    )
