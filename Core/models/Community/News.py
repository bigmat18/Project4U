from statistics import mode
from django.db import models
from django.utils.translation import gettext_lazy as _
from Core.models import AbstractImage, Post

class News(AbstractImage, Post):
    title = models.CharField(_("title"),
                            db_column="title",
                            max_length=64)
    slug = models.SlugField(blank=True, editable=False)
    intro = models.CharField(_("intro"),
                             max_length=516)
    content = models.TextField(_("content"))
    post = models.OneToOneField(Post, 
                                on_delete=models.CASCADE,
                                parent_link=True,
                                primary_key=True,
                                related_name="news",
                                related_query_name="news")
    
    class Meta:
        db_table = "news"
        verbose_name = _("News")
        verbose_name_plural = _("News")