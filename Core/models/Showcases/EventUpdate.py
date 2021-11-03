from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from Core.models import AbstractCreateUpdate, AbstractText
import uuid

class EventUpdate(AbstractCreateUpdate, AbstractText):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    author = models.ForeignKey(settings.AUTH_USER_MODEL,
                               on_delete=models.CASCADE,
                               related_name="event_updates",
                               related_query_name="event_updates")
    
    class Meta:
        db_table = "event_update"
        verbose_name = _("Event Update")
        verbose_name_plural = _("Event Updates")