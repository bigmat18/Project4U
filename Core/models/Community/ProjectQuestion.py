from django.db import models
from django.utils.translation import gettext_lazy as _
from Core.models import Post
from Core.management.scripts.generete_slug import generate_slug

class ProjectQuestion(Post):
    slug = models.SlugField(blank=True, editable=False)
    content = models.TextField()
    post = models.OneToOneField(Post, 
                                on_delete=models.CASCADE,
                                parent_link=True,
                                primary_key=True,
                                related_name="project_question",
                                related_query_name="project_question")
    
    class Meta:
        db_table = "project_question"
        verbose_name = _("Project Question")
        verbose_name_plural = _("Project Questions")
        
        
    def save(self, *args, **kwargs):
        if not self.slug: self.slug = generate_slug(self.content[:5])
        if self.type_post != "QUESTION": self.type_post = "QUESTION" 
        return super().save(*args, **kwargs)