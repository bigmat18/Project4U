from django.db import models
from django.utils.translation import gettext_lazy as _
from Core.models import AbstractComment, Post

class PostComment(AbstractComment):
    @staticmethod
    def get_author_related_name():
        return 'post_comments'
    
    @staticmethod
    def get_likes_related_name():
        return 'likes_post_comments'
    
    post = models.ForeignKey(Post,
                             on_delete=models.CASCADE,
                             related_name="comments",
                             related_query_name="comments")
    
    class Meta:
        db_table = "post_comment"
        verbose_name = _("Post Comment")
        verbose_name_plural = _("Post Comments")