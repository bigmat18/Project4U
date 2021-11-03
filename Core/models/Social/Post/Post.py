from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from Core.models import AbstractCreateUpdate

class Post(AbstractCreateUpdate):
    author = models.ForeignKey(settings.AUTH_USER_MODEL,
                               on_delete=models.CASCADE,
                               related_name="posts",
                               related_query_name="posts")
    likes_numer = models.ForeignKey(settings.AUTH_USER_MODEL,
                                    on_delete=models.CASCADE,
                                    related_name="posts_likes",
                                    related_query_name="posts_likes")
    view_number = models.PositiveBigIntegerField(_("views number"),
                                                 default=0)
    
    class Meta:
        db_table = "post"
        verbose_name = _("Post")
        verbose_name_plural = _("Posts")