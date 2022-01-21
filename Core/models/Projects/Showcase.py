from django.db import models
from django.utils import tree
from django.utils.translation import gettext_lazy as _
from Core.models import AbstractName, Project, AbstractText
from django.conf import settings
import uuid


class Showcase(AbstractName, AbstractText):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
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
                                blank=True,
                                related_name="showcases_created",
                                related_query_name="showcases_created")
    
    def save(self,*args, **kwargs):
        if self._state.adding:
            self.users.add(self.creator)
        return super().save(*args,**kwargs)
    
    class Meta:
        db_table = "showcase"
        verbose_name = _("Showcase")
        verbose_name_plural = _("Showcases")

    def __str__(self):
        return f"{str(self.project)}-{super().__str__()}"