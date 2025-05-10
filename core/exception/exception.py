from rest_framework import status
from rest_framework.exceptions import APIException


class BadRequestException(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = {"error": "invalid_request", "message": "Invalid request"}
    default_code = "invalid_request"

    def __init__(self, detail=None, code=None):
        if isinstance(detail, str):
            detail = {"detail": detail}

        super().__init__(detail=detail or self.default_detail, code=code or self.default_code)
