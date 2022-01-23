from django.db import models
from django.utils.translation import gettext_lazy as _
from Core.models import AbstractName

import uuid

class ProjectTag(AbstractName):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    searches_number_help_text = _("Numero di ricerche fatte a questo tag")
    
    searches_number = models.PositiveIntegerField(_("searches number"), default=0,
                                                  help_text=searches_number_help_text)
    
    class Meta:
        db_table = "project_tag"
        verbose_name = _("Projects Tag")
        verbose_name_plural = _("Projects Tags")

    