from django.db import models
from django.utils.translation import gettext_lazy as _
from Core.models import (AbstractImage, Idea)

class IdeaImage(AbstractImage):
    idea = models.ForeignKey(Idea,
                             on_delete=models.CASCADE,
                             related_name="images",
                             related_query_name="images")
    
    class Media:
        db_table = "idea_image"
        verbose_name = _("Idea Image")
        verbose_name_plural = _("Idea Images")