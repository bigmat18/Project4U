from django.db import models
from django.utils.translation import gettext_lazy as _
from Core.models import (AbstractComment, Idea)


class IdeaComment(AbstractComment):
    @staticmethod
    def get_author_related_name():
        return 'idea_comments'
    
    @staticmethod
    def get_likes_related_name():
        return 'likes_idea_comments'
    
    opinion = models.BooleanField(_("opinion"))
    idea = models.ForeignKey(Idea,
                             on_delete=models.CASCADE,
                             related_name="comments",
                             related_query_name="comments")
    
    class Meta:
        db_table = "idea_comment"
        verbose_name = _("Idea Comment")
        verbose_name_plural = _("Idea Comments")