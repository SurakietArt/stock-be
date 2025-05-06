from rest_framework import viewsets
from rest_framework.decorators import renderer_classes, action
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response


@renderer_classes([TemplateHTMLRenderer])
class LoginViewSet(viewsets.GenericViewSet):
    @action(detail=False, methods=["get"], url_path="login", url_name="login")
    def scan_action(self, request):
        return Response(template_name="login.html")
