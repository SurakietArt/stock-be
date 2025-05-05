from django.http import JsonResponse
from rest_framework import viewsets, mixins, status
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import action, renderer_classes
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.request import Request
from rest_framework.response import Response

from stock.dataclass.barcode_dataclass import BarcodeParam
from stock.models.items_model import Items
from stock.serializers.items_serializer import ItemsSerializer
from stock.services.items import ItemsServices


class ItemsViewSet(viewsets.ModelViewSet, viewsets.GenericViewSet):
    serializer_class = ItemsSerializer
    queryset = Items.objects.all()

    def list(self, request: Request):
        query = request.GET.get('name')
        items = Items.objects.filter(name__icontains=query)
        serialized = ItemsSerializer(items, many=True)
        return Response(serialized.data, status=status.HTTP_200_OK)

    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)

    @csrf_exempt
    @action(detail=False, methods=["post"], url_path="scan-barcode", url_name="scan-barcode")
    def scan_barcode(self, request: Request):
        params = BarcodeParam.from_post_request(request)
        return ItemsServices.scan_barcode(params)


@renderer_classes([TemplateHTMLRenderer])
class ItemTemplateViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    serializer_class = ItemsSerializer
    queryset = Items.objects.all()

    def list(self, request):
        items = Items.objects.all()
        return Response({"items": items}, template_name="main.html")

    @action(detail=False, methods=["get"], url_path="scan", url_name="scan")
    def scan_action(self, request):
        return Response(template_name="scan_form.html")
