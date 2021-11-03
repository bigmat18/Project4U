from django.db import models
from django.utils.translation import gettext_lazy as _
from Core.models import AbstractName, AbstractText
import uuid

class MillestonePost(AbstractText, AbstractName):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,editable=False)
    name = models.CharField(_("title"), 
                            db_column="title", 
                            max_length=64)
    
    class Meta:
        db_table = "millestone_post"
        verbose_name = _("Millestone Post")
        verbose_name_plural = _("Millestone Posts")
    