from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

class AbstractCreateUpdate(models.Model):
    created_at_help_text = _("Data di creazione del modello")
    updated_at_help_text = _("Data di aggiornamento del modello")
    
    created_at = models.DateTimeField(_('created at'), 
                                      default=timezone.now,
                                      editable=False,
                                      help_text=created_at_help_text)
    updated_at = models.DateTimeField(_('updated at'),
                                      editable=False,
                                      help_text=updated_at_help_text)
    
    class Meta:
        abstract = True
        ordering = ["-updated_at"]
        indexes = [models.Index(fields=['-updated_at'])]
        
    def save(self, *args, **kwargs):
        self.updated_at = timezone.now()
        return super().save(*args, **kwargs)
    
    @property
    def updated(self):
        return self.updated.strftime('%d %B %Y')
    
    @property
    def creted(self):
        return self.created_at.strftime('%d %B %Y')