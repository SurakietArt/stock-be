from django.db import models

from core.models.base_model import BaseModel
from stock.models.units_model import Units


class SalesOrder(BaseModel):
    platform = models.CharField(
        max_length=255,
        null=True,
        help_text="Which platform this order sold e.g. lazada, shopee, tiktok",
    )
    platform_customer_name = models.CharField(
        max_length=255, null=True, help_text="Name of user who brought this order"
    )
    date = models.DateField()


class SaleOrderItem(BaseModel):
    sale_order = models.ForeignKey(SalesOrder, on_delete=models.CASCADE)
    item_name = models.CharField(max_length=255)
    quantity = models.IntegerField()
    price_per_unit = models.FloatField()
    unit = models.ForeignKey(Units, on_delete=models.DO_NOTHING)
    price_sum = models.FloatField()
