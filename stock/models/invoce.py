from django.db import models

from core.models.base_model import BaseModel
from customer.models.customers_model import Customers
from stock.models.sales_order import SalesOrder


class Invoice(BaseModel):
    invoice_id = models.CharField(max_length=255)
    date = models.DateField()
    customer = models.ForeignKey(
        Customers, related_name="customer_invoice", on_delete=models.DO_NOTHING
    )
    tax_id = models.CharField(max_length=255)
    is_headquarter = models.BooleanField(default=False)
    is_branch = models.BooleanField(default=False)
    branch_num = models.CharField(max_length=255, default=None, null=True)
    sales_order = models.ForeignKey(
        SalesOrder, related_name="order_invoice", on_delete=models.DO_NOTHING
    )
    discount = models.FloatField()
