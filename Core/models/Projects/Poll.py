from django.db import models
from django.utils.translation import gettext_lazy as _
from Core.models import Message
import uuid

class Poll(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    anonymus_creator = models.BooleanField(_("anonymus creator"), default=False)
    anonymus_voters = models.BooleanField(_("anonymus voters"), default=False)
    name = models.CharField(_("name"), max_length=64)
    text = models.TextField(_("text"),max_length=516,null=True,blank=True)
    message = models.OneToOneField(Message,
                                   on_delete=models.CASCADE,
                                   related_name="poll",
                                   related_query_name="poll")
    
    class Meta:
        db_table = "poll"
        verbose_name = _("Polls")
        verbose_name_plural = _("Polls")
    
    def __str__(self): return str(self.id)