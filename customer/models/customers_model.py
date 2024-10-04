from django.db import models

from core.models.base_model import BaseModel


class Customers(BaseModel):
    name = models.CharField(max_length=255, db_index=True)
    nick_name = models.CharField(max_length=255, null=True)
    address = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=255)
    tax_id = models.CharField(max_length=255, null=True)
