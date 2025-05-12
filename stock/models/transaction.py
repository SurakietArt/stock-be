from django.db import models

from core.models.base_model import BaseModel

TRANSACTION_TYPES = (
    ('receive', 'รับเข้า'),
    ('issue', 'จ่ายออก'),
    ('update', 'อัปเดต'),
)


class ItemTransaction(BaseModel):
    item = models.ForeignKey("Items", on_delete=models.CASCADE, related_name="transactions", db_index=True)
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES, db_index=True)
    amount = models.PositiveIntegerField()
    note = models.TextField(blank=True)

    class Meta:
        ordering = ['-created_date']

    def __str__(self):
        return f"{self.transaction_type} - {self.item.name} ({self.amount})"
