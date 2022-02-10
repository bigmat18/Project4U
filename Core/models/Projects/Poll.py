from django.db import models
from django.utils.translation import gettext_lazy as _
from Core.models import Message


class Poll(Message):
    anonymus_voters = models.BooleanField(_("anonymus voters"),default=False)
    name = models.CharField(_("name"),max_length=64)
    text = models.TextField(_("text"),max_length=516,null=True,blank=True)
    message = models.OneToOneField(Message,
                                   on_delete=models.CASCADE,
                                   parent_link=True,
                                   primary_key=True,
                                   related_name="poll",
                                   related_query_name="poll")
    
    class Meta:
        db_table = "poll"
        verbose_name = _("Polls")
        verbose_name_plural = _("Polls")
    
    def __str__(self): return str(self.id)