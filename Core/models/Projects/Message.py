from django.db import models
from django.utils.translation import gettext_lazy as _
from Core.models import AbstractCreateUpdate
from django.conf import settings
import uuid

class Message(AbstractCreateUpdate):
    
    class TypeMessage(models.TextChoices):
        TEXT = "TEXT"
        EVENT = "EVENT"
        IDEA = "IDEA"
        UPDATE = "UPDATE"
        
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    showcase = models.ForeignKey("Showcase",
                                 on_delete=models.CASCADE,
                                 related_name="messages",
                                 related_query_name="messages")
    author = models.ForeignKey(settings.AUTH_USER_MODEL,
                               on_delete=models.CASCADE,
                               related_name="messages",
                               related_query_name="messages")
    type_message = models.CharField(max_length=32,
                                    choices=TypeMessage.choices)
    viewed_by = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                       related_name="messages_visualize",
                                       related_query_name="messages_visualize",
                                       blank=True)
    
    class Meta(AbstractCreateUpdate.Meta):
        db_table = "message"
        verbose_name = _("Message")
        verbose_name_plural = _("Messages")
        
    def save(self, *args, **kwargs):
        message = super().save(*args,**kwargs)
        if not self.viewed_by.filter(id=self.author.id).exists():
            self.viewed_by.add(self.author)
        return message
        
    def __str__(self): return str(self.id)
    