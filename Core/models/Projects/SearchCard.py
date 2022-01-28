from django.db import models
from django.utils.translation import gettext_lazy as _
from Core.models import Project, Skill
import uuid

class SearchCard(models.Model):
    __skills_help_text = _("Le abilità richieste nella casta di ricerca")
    
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
  
    project = models.ForeignKey(Project,
                                on_delete=models.CASCADE,
                                related_name="search_cards",
                                related_query_name="search_cards")
    skills = models.ManyToManyField(Skill,
                                   related_name="search_cards",
                                   related_query_name="search_cards",
                                   help_text=__skills_help_text)
    description = models.TextField(_("description"),null=True, blank=True)
    
    class Meta:
        db_table = "search_card"
        verbose_name = _("Search Card")
        verbose_name_plural = _("Search Cards")
        
    def __str__(self): return str(self.id)