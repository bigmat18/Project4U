from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from Core.models import Message, AbstractFile
from django.db.models import CheckConstraint, Q, F


def image_path(instance, filename):
    return f"projects/project-{instance.showcase.project.id}/"+\
           f"showcase-{instance.showcase.id}/event-{instance.id}/"+\
           f"event-image.jpg"


class Event(Message, AbstractFile):
    __started_at_help_text = _("Data inizio evento")
    __ended_at_help_text = _("Data fine evento")
    __partecipants_help_text = _("Partecipanti all'evento")
    
    image = models.ImageField(_("image"), blank=True,
                              max_length=1000,null=True,
                              upload_to=image_path)
    started_at = models.DateTimeField(_("started at"),
                                    help_text=__started_at_help_text)
    ended_at = models.DateTimeField(_("ended at"),
                                    help_text=__ended_at_help_text)
    partecipants = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                          related_name="events",
                                          related_query_name="events",
                                          help_text=__partecipants_help_text,
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
        constraints = [
            CheckConstraint(check=Q(started_at__lte=F('ended_at')),
                            name='check_event_started_at_gte')
        ]
    
    def __str__(self): return str(self.message)