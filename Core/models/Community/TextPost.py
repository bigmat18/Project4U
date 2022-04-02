from statistics import mode
from django.db import models
from django.utils.translation import gettext_lazy as _
from Core.models import Post

class TextPost(Post):
    text = models.TextField()
    
    class Meta:
        db_table = "text_post"
        verbose_name = _("Text Post")
        verbose_name_plural = _("Text Posts")