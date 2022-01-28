from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from Core.models import AbstractFile

import uuid

def image_path(instance,path):
    return f"users/user-{instance.user.id}/externals-projects_images/{instance.id}.jpg"


class ExternalProject(AbstractFile):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    image = models.ImageField(blank=True, null=True,upload_to=image_path)
    link_site = models.CharField(max_length=516, null=True, blank=True)
    name = models.CharField(_("name"), max_length=64)
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
        
    def __str__(self): return str(self.id)
