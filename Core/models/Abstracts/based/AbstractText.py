from django.db import models
from django.utils.translation import gettext_lazy as _
import uuid

class AbstractText(models.Model):
    text_help_text = _("Testo del modello")
    
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    text = models.TextField(_("text"),
                            help_text=text_help_text,
                            max_length=516)

    class Meta:
        abstract = True
        
    def __str__(self):
        if len(self.text) < 10: return self.text
        return f"{self.text[0:10]} ..."