from  django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from Core.models import AbstractName
from django.core.validators import (MaxValueValidator, 
                                    MinValueValidator) 
import uuid

class Skill(AbstractName):
    
    class TypeSkills(models.TextChoices):
        PROGRAMMING = _('Programming')
        MANAGEMENT = _('Managment')
        DESIGN = _('Design')
        OTHER = _('Other')
        
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    type_skill = models.CharField(_("type skill"), max_length=64, 
                                  default=TypeSkills.OTHER, 
                                  choices=TypeSkills.choices)
    
    class Meta:
        db_table = "skill"
        verbose_name = _("Skill")
        verbose_name_plural = _("Skills")
    
    
    
class UserSkill(models.Model):
    level_help_text = _("Livello di competenza della skill dell'utente")
    
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    skill = models.ForeignKey(Skill,
                              on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    level = models.PositiveIntegerField(default=1,
                                        validators=[MinValueValidator(1), 
                                                    MaxValueValidator(10)],
                                        help_text=level_help_text)
    
    class Meta:
        unique_together = (('skill', 'user'),)
        db_table = "user_skill"
        verbose_name = _("User Skill")
        verbose_name_plural = _("Users Skills")
        
    def __str__(self):
        return f"{self.user} - {self.skill}"
    