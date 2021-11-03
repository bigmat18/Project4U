from django.db import models
from django.utils.translation import gettext_lazy as _
from Core.models import AbstractText
import uuid

class TextPost(AbstractText):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    class Meta:
        db_table = "text_post"
        verbose_name = _("Text Post")
        verbose_name_plural = _("Text Posts")