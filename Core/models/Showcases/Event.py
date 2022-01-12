from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from Core.models import Message, AbstractText

class Event(Message, AbstractText):
    date_help_text = _("Data dell'evento")
    partecipants_help_text = _("Partecipanti all'evento")
    
    data = models.DateTimeField(_("date"),
                                help_text=date_help_text)
    partecipants = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                          related_name="events",
                                          related_query_name="events",
                                          help_text=partecipants_help_text)
    text = models.TextField(_("description"), 
                            db_column="description",
                            null=True, blank=True)
    
    class Meta:
        db_table = "event"
        verbose_name = _("Event")
        verbose_name_plural = _("Events")
    