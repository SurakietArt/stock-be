from __future__ import annotations

from dataclasses import dataclass

from django_dataclass_autoserialize import AutoSerialize


@dataclass
class OrderParam(AutoSerialize):
    item_name: str
    quantity: int
    unit_id: int
    price_per_unit: float
    price_sum: float

    @classmethod
    def example(cls, unit_id: int) -> OrderParam:
        return cls(
            item_name="น้ำพริก",
            quantity=5,
            unit_id=unit_id,
            price_per_unit=50,
            price_sum=300,
        )
