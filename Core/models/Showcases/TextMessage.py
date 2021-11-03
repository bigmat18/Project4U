from django.db import models
from django.utils.translation import gettext_lazy as _
from Core.models import Message, AbstractText

class TextMessage(Message, AbstractText):
    
    class Meta:
        db_table = "text_message"
        verbose_name = _("Text Message")
        verbose_name_plural = _("Text Messages")
    
