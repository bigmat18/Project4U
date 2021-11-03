from django.db import models
from django.db.models import indexes
from django.utils.translation import gettext_lazy as _

class AbstractName(models.Model):
    name = models.CharField(_("name"), 
                            max_length=64)

    class Meta:
        abstract = True
        ordering = ["name"]
        indexes = [models.Index(fields=["name"])]
        
    def __str__(self):
        return self.name