from django.db import models
from Core.models import AbstractName, Event
from django.utils.translation import gettext_lazy as _
import uuid


class EventTask(AbstractName):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    checked = models.BooleanField(default=False)
    event = models.ForeignKey(Event,
                              on_delete=models.CASCADE,
                              related_name="tasks",
                              related_query_name="tasks")
    
    class Meta:
        db_table = "event_task"
        verbose_name = _("EventTask")
        verbose_name_plural = _("EventTasks")