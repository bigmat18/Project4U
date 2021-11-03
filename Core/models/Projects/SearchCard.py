from django.db import models
from django.utils.translation import gettext_lazy as _
from Core.models import Project, Skill, AbstractText

class SearchCard(AbstractText):
    skills_help_text = _("Le abilità richieste nella casta di ricerca")
    
    project = models.ForeignKey(Project,
                                on_delete=models.CASCADE,
                                related_name="search_cards",
                                related_query_name="search_cards")
    skills = models.ManyToManyField(Skill,
                                   related_name="search_cards",
                                   related_query_name="search_cards",
                                   help_text=skills_help_text)
    text = models.TextField(_("description"), db_column="decription",
                            null=True, blank=True)
    
    class Meta:
        db_table = "search_card"
        verbose_name = _("Search Card")
        verbose_name_plural = _("Search Cards")
        
    
    