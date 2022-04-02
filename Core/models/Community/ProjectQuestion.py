from django.db import models
from django.utils.translation import gettext_lazy as _
from Core.models import Post

class ProjectQuestion(Post):
    slug = models.SlugField(blank=True, editable=False)
    question = models.TextField()
    
    class Meta:
        db_table = "project_question"
        verbose_name = _("Project Question")
        verbose_name_plural = _("Project Questions")