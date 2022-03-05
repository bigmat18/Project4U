from .Message import Message
from django.db import models
from django.utils.translation import gettext_lazy as _


class ShowcaseUpdate(Message):
    __type_update_help_text = _("Il tipo di aggiornamento avvenuto")
    
    __desc_default_message = _("La descrizione è stata cambiata da ")
    __color_default_message = _("Il colore della bacheca è stato modificato da ")
    __name_default_message = _("Il nome della bacheca è stato cambiato da ")
    
    class TypeUpdate(models.TextChoices):
        DESC = "DESC"
        USERS = "USERS"
        COLOR = "COLOR"
        NAME = "NAME"
        
    description = models.TextField(blank=True,null=True)
    
    type_update = models.CharField(choices=TypeUpdate.choices,max_length=16,
                                   help_text=__type_update_help_text,
                                   default=TypeUpdate.DESC)
    message = models.OneToOneField(Message, 
                                   on_delete=models.CASCADE,
                                   parent_link=True,
                                   primary_key=True,
                                   related_name="showcase_update",
                                   related_query_name="showcase_update")
    
    class Meta:
        db_table = "showcase_update"
        verbose_name = _("Showcase Upadate")
        verbose_name_plural = _("Showcase Updates")
    
    
    def save(self, *args, **kwargs):
        if self.description is None:
            if self.type_update == self.TypeUpdate.DESC:
                self.description = f"{self.__desc_default_message}{self.author.full_name}"
            elif self.type_update == self.TypeUpdate.COLOR:
                self.description = f"{self.__color_default_message}{self.author.full_name}"
            elif self.type_update == self.TypeUpdate.NAME:
                self.description = f"{self.__name_default_message}{self.author.full_name}"
        return super().save(*args, **kwargs)