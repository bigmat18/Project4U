from django.db import models
from django.utils.translation import gettext_lazy as _
from Core.models import AbstractName, AbstractImage, AbstractSlug

class News(AbstractImage, AbstractName, AbstractSlug):
    name = models.CharField(_("title"),
                            db_column="title",
                            max_length=64)
    intro = models.CharField(_("intro"),
                             max_length=516)
    content = models.TextField(_("content"))
    
    class Meta:
        db_table = "news"
        verbose_name = _("News")
        verbose_name_plural = _("News")