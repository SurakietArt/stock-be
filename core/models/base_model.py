from typing import Any

from django.conf import settings
from django.db import models
from safedelete.models import SOFT_DELETE, SafeDeleteModel


class BaseModel(SafeDeleteModel):
    _safedelete_policy = SOFT_DELETE
    created_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="%(class)s_created_by",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="%(class)s_updated_by",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    def save(self, *args: Any, **kwargs: Any) -> None:
        try:
            user = "System"  # TODO: created by user
            if not self.pk:
                # Only set added_by during the first save.
                self.created_by = user
            self.updated_by = user
        except AttributeError:
            pass

        super().save(*args, **kwargs)

    class Meta:
        abstract = True
