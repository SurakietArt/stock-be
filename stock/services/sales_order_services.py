import datetime
from typing import List

from customer.models.customers_model import Customers
from stock.dataclass.order_sales_dataclass import OrderParam
from stock.models.sales_order import SaleOrderItem, SalesOrder


class SalesOrderServices:
    @classmethod
    def create_sales_order(
        cls,
        order_param: List[OrderParam],
        platform: str,
        customer: Customers,
        date: datetime.date,
    ) -> SalesOrder:
        sales_order = SalesOrder.objects.create(
            platform=platform, platform_customer_name=customer.name, date=date
        )
        all_sales_order_item: List[SaleOrderItem] = list()
        for each_order_param in order_param:
            sales_order_item = SaleOrderItem(
                sales_order=sales_order,
                item=each_order_param.item_name,
                quantity=each_order_param.quantity,
                price_per_unit=each_order_param.price_per_unit,
                unit_id=each_order_param.unit_id,
                price_sum=each_order_param.price_sum,
            )
            all_sales_order_item.append(sales_order_item)
        SaleOrderItem.objects.bulk_create(all_sales_order_item)
        return sales_order
