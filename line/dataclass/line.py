from __future__ import annotations
from dataclasses import dataclass
from datetime import time
from typing import List

from django.conf import settings
from django.utils import timezone
from django_dataclass_autoserialize import AutoSerialize

from stock.models.items_model import Items

THAI_MONTHS = [
    "",  # padding for 1-indexed months
    "มกราคม", "กุมภาพันธ์", "มีนาคม", "เมษายน", "พฤษภาคม", "มิถุนายน",
    "กรกฎาคม", "สิงหาคม", "กันยายน", "ตุลาคม", "พฤศจิกายน", "ธันวาคม",
]


@dataclass
class LineAccess(AutoSerialize):
    grant_type: str
    code: str
    redirect_uri: str
    client_id: str
    client_secret: str

    @classmethod
    def example(cls) -> LineAccess:
        return cls(
            grant_type="authorization_code",
            code="code",
            redirect_uri="redirect_uri",
            client_id="client_id",
            client_secret="client_secret"
        )

    @classmethod
    def get_data(cls, code: str) -> LineAccess:
        return cls(
            grant_type="authorization_code",
            code=code,
            redirect_uri=settings.LINE_LOGIN_REDIRECT_URI,
            client_id=settings.LINE_LOGIN_CLIENT_ID,
            client_secret=settings.LINE_LOGIN_CHANNEL_SECRET
        )


@dataclass
class LineMulticastRequest(AutoSerialize):
    to: List[str]
    messages: List[LineMessage]

    @classmethod
    def build_alert_threshold_message(cls, items: List[Items], include_date: bool = False) -> LineMulticastRequest:
        line_message = LineMessage(
            text=cls.build_message_from_items(items, include_date),
        )
        return LineMulticastRequest(to=settings.LINE_USER_GET_ALERT_THRESHOLD, messages=[line_message])

    @classmethod
    def build_message_from_items(cls, items: List["Items"], include_date: bool = False) -> str:
        header = "ของใก้ลหมด"

        if include_date:
            now = timezone.now()
            thai_date_str = f"{now.day:02d} {THAI_MONTHS[now.month]} {now.year}"
            header = f"สรุปของใก้ลหมด ประจำวันที่ {thai_date_str}"

        lines = [header]
        for item in items:
            lines.append(
                f"{item.name}: คงเหลือ {item.amount} \n(จำนวนที่แจ้งเตือน {item.alert_threshold})\n"
            )

        return "\n".join(lines)


@dataclass
class LineMessage(AutoSerialize):
    text: str
    type: str = "text"
