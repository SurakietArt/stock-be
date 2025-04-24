from __future__ import annotations

from dataclasses import dataclass

from django_dataclass_autoserialize import AutoSerialize


@dataclass
class BarcodeParam(AutoSerialize):
    barcode: str
    amount: int
    action: str

    @classmethod
    def example(cls) -> BarcodeParam:
        return cls(
            barcode="1234",
            amount=1,
            action="receive"
            )
