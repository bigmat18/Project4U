from django.db import models
from django.utils import tree
from django.utils.translation import gettext_lazy as _
from Core.models import Project
from django.conf import settings
import uuid


class Showcase(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    name = models.CharField(_("name"), max_length=64)
    description = models.TextField(_("description"),max_length=516,null=True,blank=True)
    project = models.ForeignKey(Project,
                                on_delete=models.CASCADE,
                                related_name="showcases",
                                related_query_name="showcases")
    users = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                   related_name="showcases",
                                   related_query_name="showcases",
                                   blank=True)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL,
                                on_delete=models.SET_NULL,
                                null=True,
                                related_name="showcases_created",
                                related_query_name="showcases_created")
    
    class Meta:
        db_table = "showcase"
        verbose_name = _("Showcase")
        verbose_name_plural = _("Showcases")
        
    def save(self,*args, **kwargs):
        adding = self._state.adding
        showcase = super().save(*args,**kwargs)
        if adding: self.users.add(self.creator)
        return showcase

    def __str__(self): return f"{self.project}-{self.name}"