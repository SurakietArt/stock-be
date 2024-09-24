from django.db import models

from core.models.base_model import BaseModel


class SalesOrder(BaseModel):
    order_id = models.CharField(max_length=255, db_index=True)
    platform = models.CharField(
        max_length=255,
        help_text="Which platform this order sold e.g. lazada, shopee, tiktok",
    )
    platform_customer_name = models.CharField(
        max_length=255, null=True, help_text="Name of user who brought this order"
    )
    date = models.DateField()


class SaleOrderItem(models.Model):
    sale_order = models.ForeignKey(SalesOrder, on_delete=models.CASCADE)
    item_name = models.CharField(max_length=255)
    quantity = models.IntegerField()
    price_per_unit = models.FloatField()
    price_sum = models.FloatField()

    class Meta:
        unique_together = ("sale_order", "item")
