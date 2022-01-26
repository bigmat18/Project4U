from django.db import models
from django.utils.translation import gettext_lazy as _
import uuid

class AbstractImage(models.Model):
    caption_help_text = _("Didascalia descrittiva dell'immagine")
    
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    image = models.ImageField(_("image"))
    caption = models.CharField(_("caption"),max_length=256,
                                blank=True, null=True,
                                help_text=caption_help_text)
    
    class Meta:
        abstract = True
    