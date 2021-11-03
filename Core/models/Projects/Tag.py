from django.db import models
from django.utils.translation import gettext_lazy as _
from Core.models import AbstractName

class Tag(AbstractName):
    searches_number_help_text = _("Numero di ricerche fatte a questo tag")
    
    searches_number = models.PositiveIntegerField(_("searches number"), default=0,
                                                  help_text=searches_number_help_text)
    
    class Meta:
        db_table = "tag"
        verbose_name = _("Tag")
        verbose_name_plural = _("Tags")

    