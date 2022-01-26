from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from Core.models import Message

class Event(Message):
    date_help_text = _("Data dell'evento")
    partecipants_help_text = _("Partecipanti all'evento")
    
    date = models.DateTimeField(_("date"),
                                help_text=date_help_text)
    partecipants = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                          related_name="events",
                                          related_query_name="events",
                                          help_text=partecipants_help_text,
                                          blank=True)
    description = models.TextField(_("description"),null=True, blank=True)
    message = models.OneToOneField(Message, 
                                   on_delete=models.CASCADE,
                                   parent_link=True,
                                   primary_key=True,
                                   related_name="event",
                                   related_query_name="event")
    
    class Meta:
        db_table = "event"
        verbose_name = _("Event")
        verbose_name_plural = _("Events")
    
    def __str__(self): return str(self.message)