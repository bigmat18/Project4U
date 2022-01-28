from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.db.models import CheckConstraint, Q, F


class AbstractCreateUpdate(models.Model):
    __default_format = "YY - MM - GG"
    __created_at_help_text = _("Data di creazione del modello")
    __updated_at_help_text = _("Data di aggiornamento del modello")
    
    created_at = models.DateTimeField(_('created at'),
                                      null=True,
                                      default=None,
                                      editable=False,
                                      help_text=__created_at_help_text)
    updated_at = models.DateTimeField(_('updated at'),
                                      null=True,
                                      default=None,
                                      editable=False,
                                      help_text=__updated_at_help_text)
    
    class Meta:
        abstract = True
        ordering = ["-updated_at"]
        constraints = [
            CheckConstraint(check=Q(updated_at__gte=F('created_at')),
                            name='check_%(class)s_updated_at')
        ]
    
    @property
    def is_updated(self):
        return self.created_at.strftime(self.__default_format)
    
    @property
    def is_creted(self):
        return self.created_at.strftime(self.__default_format)
    
    
    def save(self, *args, **kwargs):
        self.set_created_at()
        self.set_update_at()
        return super().save(*args, **kwargs)
    
    def set_created_at(self):
        if self.created_at is None:
            self.created_at = timezone.now()
            
    def set_update_at(self):
        self.updated_at = timezone.now()