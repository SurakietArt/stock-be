from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from django_dataclass_autoserialize import AutoSerialize


@dataclass
class CustomerParam(AutoSerialize):
    id: Optional[int]
    name: str
    address: str
    phone_number: str
    tax_id: str

    @classmethod
    def example(cls) -> CustomerParam:
        return cls(
            id=None,
            name="นาย ทดสอบ ระบบ",
            address="บ้านเลขที่ ซอย แขวง เขต กรุงเทพ 10220",
            phone_number="081-234-5678",
            tax_id="123-456-789",
        )
