from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from Core.models import AbstractCreateUpdate, ProjectQuestion
import uuid

class ProjectAnswer(AbstractCreateUpdate):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    author = models.ForeignKey(settings.AUTH_USER_MODEL,
                               on_delete=models.CASCADE,
                               related_name="project_answers",
                               related_query_name="project_answers")
    question = models.ForeignKey(ProjectQuestion,
                                 on_delete=models.CASCADE,
                                 related_name="answers",
                                 related_query_name="answers")
    content = models.TextField()
    
    class Meta:
        db_table = "project_answer"
        verbose_name = _("Project Answer")
        verbose_name_plural = _("Project Answers")