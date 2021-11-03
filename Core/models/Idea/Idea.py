from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from Core.models import (AbstractCreateUpdate, AbstractText, 
                         AbstractName, Project, Message)


class Idea(AbstractCreateUpdate, AbstractText, AbstractName):
    message_help_text = _("Il collegamento al messagio nel caso l'idea sia pubblicata in una bacheca")
    project_help_text = _("Il collegamento al progetto serve quando l'idea è pubblica sulla parte social")
    
    author = models.ForeignKey(settings.AUTH_USER_MODEL,
                               on_delete=models.CASCADE,
                               related_name="ideas",
                               related_query_name="ideas")
    project = models.ForeignKey(Project,
                                on_delete=models.SET_NULL,
                                null=True, blank=True,
                                related_name="ideas",
                                related_query_name="ideas")
    message = models.ForeignKey(Message,
                                on_delete=models.SET_NULL,
                                related_name="ideas",
                                related_query_name="ideas",
                                null=True, blank=True)
    
    class Meta:
        db_table = "idea"
        verbose_name = _("Idea")
        verbose_name_plural = _("Ideas")