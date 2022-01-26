from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from Core.models import Poll
import uuid

class PollOption(models.Model):
    votes_help_text = _("I voti dati all'opzione del sondaggio")
    
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    text = models.TextField(_("text"),max_length=516,null=True,blank=True)
    poll = models.ForeignKey(Poll,
                             on_delete=models.CASCADE,
                             related_name="options",
                             related_query_name="options")
    votes = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                   related_name="poll_option_votes",
                                   related_query_name="poll_option_votes",
                                   help_text=votes_help_text)
    
    class Meta:
        db_table = "poll_option"
        verbose_name = _("Poll Option")
        verbose_name_plural = _("Poll Options")
        
    def __str__(self): return str(self.id)