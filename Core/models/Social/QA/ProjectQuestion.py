from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from Core.models import (AbstractCreateUpdate, AbstractText, 
                         AbstractSlug, Project)
import uuid

class ProjectQuestion(AbstractCreateUpdate, 
                      AbstractText, 
                      AbstractSlug):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    author = models.ForeignKey(settings.AUTH_USER_MODEL,
                               on_delete=models.CASCADE,
                               related_name="project_questions",
                               related_query_name="proejct_questions")
    project = models.ForeignKey(Project,
                                on_delete=models.CASCADE,
                                related_name="questions",
                                related_query_name="questions")
    
    class Meta:
        db_table = "project_question"
        verbose_name = _("Project Question")
        verbose_name_plural = _("Project Questions")