from django.db import models
from django.utils.translation import gettext_lazy as _
from Core.models import (AbstractComment, IdeaComment)

class IdeaSubComment(AbstractComment):
    @staticmethod
    def get_author_related_name():
        return 'idea_subcomments'
    
    @staticmethod
    def get_likes_related_name():
        return 'likes_idea_subcomments'
    
    comment = models.ForeignKey(IdeaComment,
                                on_delete=models.CASCADE,
                                related_name="subcomments",
                                related_query_name="subcomments")
    
    class Meta:
        db_table = "idea_subcomment"
        verbose_name = _("Idea SubComment")
        verbose_name_plural = _("Idea SubComments")
