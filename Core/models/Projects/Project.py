from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from Core.models import (AbstractCreateUpdate,
                         Tag, AbstractName, 
                         AbstractText)


class Project(AbstractText, AbstractName, AbstractCreateUpdate):
    link_site_help_text = _("Link del sito di contatto del progetto")
    ended_at_help_text = _("Data di chiusura del progetto. Se null il progetto è aperto")
    num_swipe_help_text = _("Il numero di swipe fatti dal progetto")
    tags_help_text = _("I tags che identificano il progetto")
    
    creator = models.ForeignKey(settings.AUTH_USER_MODEL,
                                on_delete=models.SET_NULL,
                                null=True,
                                related_name="projects_created",
                                related_query_name="projects_created")
    
    image = models.ImageField(_("image"), blank=True, null=True)
    link_site = models.TextField(_("link site"), blank=True, null=True,
                                 help_text=link_site_help_text,
                                 max_length=516)
    
    ended_at = models.DateTimeField(_("ended"),null=True, blank=True,
                                    help_text=ended_at_help_text)
    num_swipe = models.PositiveBigIntegerField(_("number swipe"), default=0,
                                               help_text=num_swipe_help_text)
    
    text = models.TextField(_("description"), 
                            db_column="description",
                            null=True, blank=True)
    
    tags = models.ManyToManyField(Tag,
                                  related_name="projects",
                                  related_query_name="projects",
                                  help_text=tags_help_text)
    
    users = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                   through="UserProject",
                                   through_fields=("project", "user"),
                                   related_name="projects",
                                   related_query_name="projects")
    
    class Meta:
        db_table = "project"
        verbose_name = _("Project")
        verbose_name_plural = _("Projects")
    
    @property
    def ended(self):
        return self.ended_at.strftime('%d %B %Y')