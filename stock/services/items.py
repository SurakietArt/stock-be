from typing import Optional

from rest_framework import status
from rest_framework.response import Response

from core.exception.exception import BadRequestException
from core.models import Users
from stock.constant import TRANSACTION_TYPE_RECEIVE
from stock.dataclass.barcode_dataclass import BarcodeParam, BarcodeResponse
from stock.models.items_model import Items
from stock.models.transaction import ItemTransaction


class ItemsServices:

    @classmethod
    def get_items(cls, name: Optional[None]) -> Items:
        if name:
            items = Items.objects.filter(name__icontains=name)
        else:
            items = Items.objects.all()
        return items

    @classmethod
    def create_item_transaction(cls, user: Users, item: Items, transaction_type: str, amount: int):
        ItemTransaction.objects.create(
            item=item,
            transaction_type=transaction_type,
            amount=amount,
            created_by=user,
        )

    @classmethod
    def amount_checker(cls, item: Items, params: BarcodeParam) -> None:
        item_before = item.amount
        item.amount -= params.amount

        if item.amount < 0:
            raise BadRequestException(BarcodeResponse(
                    name=item.name,
                    message=f"❌ จำนวนไม่ถูกต้อง (คงเหลือ {item_before})",
                    current_amount=item.amount).to_data())
        return None

    @classmethod
    def scan_barcode(cls, params: BarcodeParam, user: Users) -> Response:
        try:
            item = Items.objects.get(barcode=params.barcode)
            cls.create_item_transaction(user, item, params.action, params.amount)
            cls.amount_checker(item, params)
            item.save()
            return Response(
                BarcodeResponse(
                    name=item.name,
                    message=f"✅ ดำเนินการ {'รับเข้า' if params.action == TRANSACTION_TYPE_RECEIVE else 'จ่ายออก'} สำเร็จ",
                    current_amount=item.amount).to_data(),
                status.HTTP_200_OK)

        except Items.DoesNotExist:
            return Response(
                BarcodeResponse(
                    name="",
                    message="❌ ไม่พบสินค้าในระบบ",
                    current_amount=0).to_data(),
                status.HTTP_404_NOT_FOUND)
