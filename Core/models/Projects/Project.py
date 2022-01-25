from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from Core.models import (AbstractCreateUpdate,
                         ProjectTag, AbstractName, 
                         AbstractText)

from django.dispatch import receiver
from django.db.models.signals import pre_save, pre_delete
from storages.backends.s3boto3 import S3Boto3Storage

def image_path(instance, filename):
    return f"projects/project-{instance.id}/project-image.jpg"


class Project(AbstractName, AbstractText, AbstractCreateUpdate):
    link_site_help_text = _("Link del sito di contatto del progetto")
    ended_at_help_text = _("Data di chiusura del progetto. Se null il progetto è aperto")
    num_swipe_help_text = _("Il numero di swipe fatti dal progetto")
    tags_help_text = _("I tags che identificano il progetto")
    
    creator = models.ForeignKey(settings.AUTH_USER_MODEL,
                                on_delete=models.SET_NULL,
                                null=True,
                                related_name="projects_created",
                                related_query_name="projects_created")
    
    name = models.CharField(_("name"), unique=True,max_length=64)
    
    image = models.ImageField(_("image"), blank=True, null=True,upload_to=image_path)
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
    
    tags = models.ManyToManyField(ProjectTag,
                                  related_name="projects",
                                  related_query_name="projects",
                                  help_text=tags_help_text,
                                  blank=True)
    
    users = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                   through="UserProject",
                                   through_fields=("project", "user"),
                                   related_name="projects",
                                   related_query_name="projects")
    def save(self,*args, **kwargs):
        from .Showcase import Showcase
        adding = self._state.adding
        project = super().save(*args,**kwargs)
        if adding:
            Showcase.objects.create(name="Generali",creator=self.creator,project=self)
            Showcase.objects.create(name="Idee",creator=self.creator,project=self)
            self.users.add(self.creator)
        return project
    
    class Meta:
        db_table = "project"
        verbose_name = _("Project")
        verbose_name_plural = _("Projects")
    
    @property
    def ended(self):
        return self.ended_at.strftime('%d %B %Y')

    
    
if not settings.DEBUG:
    @receiver(pre_delete,sender=Project)
    def pre_delete_image(sender, instance, *args, **kwargs):
        if instance.image:
            storage = S3Boto3Storage()
            storage.delete(str(instance.image))

    @receiver(pre_save, sender=Project)
    def pre_save_image(sender, instance, *args, **kwargs):
        project = Project.objects.filter(id=instance.id)
        if project.exists():
            project = project.get(id=instance.id)
            storage = S3Boto3Storage()
            if not instance.image and project.image:
                storage.delete(str(project.image))