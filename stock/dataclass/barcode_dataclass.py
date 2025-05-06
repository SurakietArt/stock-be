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


@dataclass
class BarcodeResponse(AutoSerialize):
    name: str
    message: str
    current_amount: int

    @classmethod
    def example(cls) -> BarcodeResponse:
        return cls(
            name="น้ำพริกมันกุ้ง",
            message="ดำเนินการรับเข้าสำเร็จ",
            current_amount=1
        )
