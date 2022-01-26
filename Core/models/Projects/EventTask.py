from django.db import models
from Core.models import Event
from django.utils.translation import gettext_lazy as _
import uuid


class EventTask(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    checked = models.BooleanField(default=False)
    name = models.CharField(_("name"), max_length=64)
    event = models.ForeignKey(Event,
                              on_delete=models.CASCADE,
                              related_name="tasks",
                              related_query_name="tasks")
    
    class Meta:
        db_table = "event_task"
        verbose_name = _("Event Task")
        verbose_name_plural = _("Event Tasks")
        
    def __str__(self): return str(self.id)