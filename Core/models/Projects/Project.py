from email.policy import default
from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from Core.models import (AbstractCreateUpdate, ProjectTag, AbstractFile)
from .Showcase import Showcase

from django.db.models import CheckConstraint, Q, F
from django.db.models.functions import Now

import uuid


def image_path(instance, filename):
    return f"projects/project-{instance.id}/project-image.jpg"

class Project(AbstractFile,AbstractCreateUpdate):
    __link_site_help_text = _("Link del sito di contatto del progetto")
    __ended_at_help_text = _("Data di chiusura del progetto. Se null il progetto è aperto")
    __num_swipe_help_text = _("Il numero di swipe fatti dal progetto")
    __tags_help_text = _("I tags che identificano il progetto")
    
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL,
                                on_delete=models.SET_NULL,
                                null=True,
                                related_name="projects_created",
                                related_query_name="projects_created")
    
    name = models.CharField(_("name"),unique=True,max_length=64)
    description = models.TextField(_("description"),max_length=516,null=True,blank=True)

    
    image = models.ImageField(_("image"), blank=True, null=True,upload_to=image_path)
    link_site = models.TextField(_("link site"), blank=True, null=True,
                                 help_text=__link_site_help_text,
                                 max_length=516)
    
    ended_at = models.DateField(_("ended"),null=True, blank=True,
                                    help_text=__ended_at_help_text)
    num_swipe = models.PositiveBigIntegerField(_("number swipe"), default=0,
                                               help_text=__num_swipe_help_text)
    
    tags = models.ManyToManyField(ProjectTag,
                                  related_name="projects",
                                  related_query_name="projects",
                                  help_text=__tags_help_text,
                                  blank=True)
    
    users = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                   through="UserProject",
                                   through_fields=("project", "user"),
                                   related_name="projects",
                                   related_query_name="projects")
    
    class Meta(AbstractCreateUpdate.Meta):
        db_table = "project"
        verbose_name = _("Project")
        verbose_name_plural = _("Projects")
        constraints = [
            CheckConstraint(check=Q(ended_at__lte=Now()),name="check_ended_at"),
            CheckConstraint(check=Q(updated_at__gte=F('created_at')),name="check_project_updated_at")
        ]
    
    @property
    def ended(self):
        return self.ended_at.strftime('%d %B %Y')
    
    def save(self,*args, **kwargs):
        project = super().save(*args,**kwargs)
        self.setup_default_showcase()
        self.setup_creator()
        return project
    
    def setup_default_showcase(self):
        if not Showcase.objects.filter(project=self,name="Generale").exists():
            Showcase.objects.create(name="Generale",creator=self.creator,
                                    project=self,default=True)
        if not Showcase.objects.filter(project=self,name="Idee").exists():
            Showcase.objects.create(name="Idee",creator=self.creator,
                                    project=self,default=True) 
    
    def setup_creator(self):
        if not self.users.filter(id=self.creator.id).exists():
            self.users.add(self.creator)
    
    def __str__(self): return f"{self.name}"