from django.db import models
from django.utils.translation import gettext_lazy as _
from Core.models import AbstractImage, NewsParagraph

class NewsParagraphImage(AbstractImage):
    paragraph = models.ForeignKey(NewsParagraph,
                                  on_delete=models.CASCADE,
                                  related_name="images",
                                  related_query_name="images")
    class Meta:
        db_table = "news_paragraph_image"
        verbose_name = _("News Paragraph Image")
        verbose_name_plural = _("News Paragraph Images")