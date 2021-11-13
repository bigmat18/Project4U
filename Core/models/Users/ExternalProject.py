from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from Core.models import AbstractName, AbstractText
import uuid

class ExternalProject(AbstractName):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    image = models.ImageField(blank=True, null=True)
    link_site = models.CharField(max_length=516, null=True, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE,
                             related_name="external_projects",
                             related_query_name="external_projects")
    description = models.TextField(_("description"),max_length=512,
                                   blank=True, null=True)
    
    class Meta:
        db_table = "external_project"
        verbose_name = _("External Project")
        verbose_name_plural = _("External Projects")
    