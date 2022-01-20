from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from Core.models import AbstractName

from django.dispatch import receiver
from django.db.models.signals import pre_save, pre_delete
from storages.backends.s3boto3 import S3Boto3Storage

from django.core.exceptions import ValidationError

import uuid

def image_path(instance,path):
    return f"users/user-{instance.user.id}/externals-projects_images/{instance.id}.jpg"


class ExternalProject(AbstractName):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    image = models.ImageField(blank=True, null=True,upload_to=image_path)
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
    
    
@receiver(pre_delete,sender=ExternalProject)
def pre_delete_image(sender, instance, *args, **kwargs):
    if instance.image:
        storage = S3Boto3Storage()
        storage.delete(str(instance.image))

@receiver(pre_save, sender=ExternalProject)
def pre_save_image(sender, instance, *args, **kwargs):
    project = ExternalProject.objects.filter(id=instance.id)
    if project.exists():
        project = project.get(id=instance.id)
        storage = S3Boto3Storage()
        if not instance.image and project.image:
            storage.delete(str(project.image))