from typing import Optional

from django.db import DatabaseError
from rest_framework import status
from rest_framework.response import Response

from core.exception.exception import BadRequestException, InternalErrorException
from core.models import Users
from stock.constant import TRANSACTION_TYPE_RECEIVE, TRANSACTION_TYPE_ISSUE, TRANSACTION_TYPE_UPDATE
from stock.dataclass.barcode_dataclass import BarcodeParam, BarcodeResponse
from stock.models.items_model import Items
from stock.models.transaction import ItemTransaction


class ItemsServices:

    @classmethod
    def get_items(cls, name: Optional[str]) -> Items:
        if name:
            items = Items.objects.filter(name__icontains=name)
        else:
            items = Items.objects.all()
        return items

    @classmethod
    def create_item_transaction(cls, user: Users, item: Items, transaction_type: str, amount: int) -> ItemTransaction:
        ret = ItemTransaction.objects.create(
            item=item,
            transaction_type=transaction_type,
            amount=amount,
            created_by=user,
        )
        return ret

    @classmethod
    def update_item(cls, item: Items, amount: int, alert_threshold: Optional[int]) -> Items:
        item.amount = amount
        if alert_threshold:
            item.alert_threshold = alert_threshold
        item.save()
        return item

    @classmethod
    def get_final_amount(cls, transaction_type: str, item: Items, amount: int) -> int:
        if transaction_type == TRANSACTION_TYPE_RECEIVE:
            final_amount = item.amount + amount
        elif transaction_type == TRANSACTION_TYPE_ISSUE:
            final_amount = item.amount - amount
            cls.amount_checker(item, final_amount)
        elif transaction_type == TRANSACTION_TYPE_UPDATE:
            final_amount = amount
            cls.amount_checker(item, final_amount)
        else:
            raise BadRequestException(f"Invalid transaction type "
                                      f"({TRANSACTION_TYPE_RECEIVE}, "
                                      f"{TRANSACTION_TYPE_ISSUE}, "
                                      f"{TRANSACTION_TYPE_UPDATE})")
        return final_amount

    @classmethod
    def save_item_with_transaction(
            cls, user: Users, item: Items, transaction_type: str, amount: int, alert_threshold: Optional[int]) -> Items:
        transaction = None
        final_amount = cls.get_final_amount(transaction_type, item, amount)
        if alert_threshold is not None:
            transaction = cls.create_item_transaction(user, item, transaction_type, amount)
        try:
            item = cls.update_item(item, final_amount, alert_threshold)
        except DatabaseError as e:
            if transaction:
                transaction.delete()
            raise InternalErrorException(e)
        return item

    @classmethod
    def amount_checker(cls, item: Items, final_amount: int) -> None:
        if final_amount < 0:
            raise BadRequestException(BarcodeResponse(
                    name=item.name,
                    message=f"❌ จำนวนไม่ถูกต้อง (คงเหลือ {item.amount})",
                    current_amount=item.amount).to_data())
        return None

    @classmethod
    def scan_barcode(cls, params: BarcodeParam, user: Users) -> Response:
        try:
            item = Items.objects.get(barcode=params.barcode)
            cls.save_item_with_transaction(user, item, params.action, params.amount, None)
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
