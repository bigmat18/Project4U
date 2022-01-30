from django.db import models
from django.utils.translation import gettext_lazy as _
from Core.models import Message

class TextMessage(Message):
    text = models.TextField(_("text"),max_length=516,null=True,blank=True)
    message = models.OneToOneField(Message, 
                                   on_delete=models.CASCADE,
                                   parent_link=True,
                                   primary_key=True,
                                   related_name="text_message",
                                   related_query_name="text_message")
    class Meta:
        db_table = "text_message"
        verbose_name = _("Text Message")
        verbose_name_plural = _("Text Messages")
    
    def __str__(self): return str(self.author)