from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.db.models import CheckConstraint, Q
import uuid

class Skill(models.Model):
    
    class TypeSkills(models.TextChoices):
        PROGRAMMING = 'Programming'
        MANAGEMENT = 'Managment'
        DESIGN = 'Design'
        OTHER = 'Other'
        
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    name = models.CharField(_("name"), max_length=64, unique=True)
    type_skill = models.CharField(_("type skill"), max_length=64, 
                                  default=TypeSkills.OTHER, 
                                  choices=TypeSkills.choices)
    
    class Meta:
        db_table = "skill"
        verbose_name = _("Skill")
        verbose_name_plural = _("Skills")

    def __str__(self): return str(self.name)

    
    
    
class UserSkill(models.Model):
    level_help_text = _("Livello di competenza della skill dell'utente")
    
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    skill = models.ForeignKey(Skill,
                              on_delete=models.CASCADE,
                              related_name="user_skill",
                              related_query_name="user_skill")
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE,
                             related_name="user_skill",
                            related_query_name="user_skill")
    level = models.PositiveIntegerField(default=1,
                                        help_text=level_help_text)
    
    class Meta:
        unique_together = (('skill', 'user'),)
        db_table = "user_skill"
        verbose_name = _("User Skill")
        verbose_name_plural = _("Users Skills")
        constraints = [
            CheckConstraint(check=Q(Q(level__gte=1) & Q(level__lte=5)),
                            name="check_user_skill_level")
        ]
        
    def __str__(self): return f"{self.user} - {self.skill}"
    