from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional

from django_dataclass_autoserialize import AutoSerialize

from stock.dataclass.order_sales_dataclass import OrderParam


@dataclass
class InvoiceParam(AutoSerialize):
    date: datetime.date
    customer_id: int
    is_headquarter: bool
    is_branch: bool
    branch_num: Optional[int]
    orders: List[OrderParam]
    discount: float

    @classmethod
    def example(cls, customer_id: int = 1) -> InvoiceParam:
        return cls(
            date=datetime.strptime("11/22/2566", "%d/%m/%y"),
            customer_id=customer_id,
            is_headquarter=True,
            is_branch=False,
            branch_num=None,
            orders=[OrderParam.example(unit_id=1)],
            discount=20.3,
        )
