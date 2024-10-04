from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from stock.dataclass.invoice_dataclass import InvoiceParam
from stock.models.items_model import Items
from stock.serializers.invoice_serializer import InvoiceSerializer
from stock.services.invoice_services import InvoiceServices


class InvoiceViewSet(ModelViewSet):
    serializer_class = InvoiceSerializer
    queryset = Items.objects.all()

    def create(self, request: Request, *args, **kwargs) -> Response:
        invoice_param = InvoiceParam.from_post_request(request)
        new_invoice = InvoiceServices.create_invoice(invoice_param)
        return Response(
            data=InvoiceSerializer(new_invoice).data, status=status.HTTP_201_CREATED
        )
