from django.db import models
from django.utils.translation import gettext_lazy as _

import uuid

class ProjectTag(models.Model):
    __searches_number_help_text = _("Numero di ricerche fatte a questo tag")
    
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    name = models.CharField(_("name"), max_length=64)
    searches_number = models.PositiveBigIntegerField(_("searches number"), default=0,
                                                  help_text=__searches_number_help_text)
    
    class Meta:
        db_table = "project_tag"
        verbose_name = _("Projects Tag")
        verbose_name_plural = _("Projects Tags")

    def __str__(self): return str(self.id)