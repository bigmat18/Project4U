from django.db import models
from django.utils.translation import gettext_lazy as _
from Core.models import AbstractFile

class AbstractImage(AbstractFile):
    __caption_help_text = _("Didascalia descrittiva dell'immagine")
    
    image = models.ImageField(_("image"))
    caption = models.CharField(_("caption"),max_length=256,
                                blank=True, null=True,
                                help_text=__caption_help_text)
    
    class Meta:
        abstract = True
    