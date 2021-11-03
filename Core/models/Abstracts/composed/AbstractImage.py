from django.db import models
from django.utils.translation import gettext_lazy as _
from Core.models import AbstractText
import uuid

class AbstractImage(AbstractText):
    caption_help_text = _("Didascalia descrittiva dell'immagine")
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    image = models.ImageField(_("image"))
    text = models.CharField(_("caption"), db_column="caption",
                            max_length=256,
                            blank=True, null=True,
                            help_text=caption_help_text)
    
    class Meta:
        abstract = True
    