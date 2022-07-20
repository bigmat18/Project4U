from django.db import models
from django.utils.translation import gettext_lazy as _
from Core.models import Post, AbstractFile

def file_path(instace,filename):
    return f"projects/project-{instace.post.project.id}"+\
           f"/posts/text/{filename}"

class TextPost(Post, AbstractFile):
    text = models.TextField()
    file = models.FileField(upload_to=file_path,
                            max_length=1000,
                            blank=True,
                            null=True)
    post = models.OneToOneField(Post, 
                                on_delete=models.CASCADE,
                                parent_link=True,
                                primary_key=True,
                                related_name="text_post",
                                related_query_name="text_post")
    
    class Meta:
        db_table = "text_post"
        verbose_name = _("Text Post")
        verbose_name_plural = _("Text Posts")
        
    def save(self, *args, **kwargs):
        if self.type_post != "TEXT": self.type_post = "TEXT" 
        return super().save(*args, **kwargs)