from rest_framework import status
from rest_framework.response import Response

from stock.dataclass.barcode_dataclass import BarcodeParam
from stock.models.items_model import Items
from stock.models.transaction import ItemTransaction


class ItemsServices:

    @classmethod
    def scan_barcode(cls, params: BarcodeParam) -> Response:
        try:
            item = Items.objects.get(barcode=params.barcode)

            ItemTransaction.objects.create(
                item=item,
                transaction_type=params.action,
                amount=params.amount,
            )
            item_before = item.amount
            if params.action == "receive":
                item.amount += params.amount
            elif params.action == "issue":
                item.amount -= params.amount

            if item.amount < 0:
                return Response(
                    {"message": f"❌ จำนวนไม่ถูกต้อง (คงเหลือ {item_before})"},
                    status.HTTP_400_BAD_REQUEST)
            item.save()

            return Response(
                {"message": f"✅ ดำเนินการ {'รับเข้า' if params.action == 'receive' else 'จ่ายออก'} สำเร็จ"},
                status.HTTP_200_OK)

        except Items.DoesNotExist:
            return Response(
                {"message": "❌ ไม่พบสินค้าในระบบ"},
                status.HTTP_404_NOT_FOUND)
