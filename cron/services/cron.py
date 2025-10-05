from django.db.models import F

from line.dataclass.line import LineMulticastRequest
from line.services.line_services import LineService
from stock.models.items_model import Items


class CronJobServices:
    @classmethod
    def items_alert_threshold(cls):
        items = Items.objects.filter(
            alert_threshold__isnull=False,
            amount__lt=F('alert_threshold')
        )
        message = LineMulticastRequest.build_alert_threshold_message(items, True)
        LineService.send_multicast_message_to_users(message)


def items_alert_threshold():
    CronJobServices.items_alert_threshold()
