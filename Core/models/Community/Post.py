from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from Core.models import AbstractCreateUpdate, Project
import uuid

class Post(AbstractCreateUpdate):
    
    class TypePost(models.TextChoices):
        TEXT = "TEXT"
        NEWS = "NEWS"
        QUESTION = "QUESTION"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    type_post = models.CharField(max_length=16, choices=TypePost.choices, default=TypePost.TEXT)
    author = models.ForeignKey(settings.AUTH_USER_MODEL,
                               on_delete=models.CASCADE,
                               related_name="posts",
                               related_query_name="posts")
    likes = models.ForeignKey(settings.AUTH_USER_MODEL,
                                    on_delete=models.CASCADE,
                                    related_name="posts_likes",
                                    related_query_name="posts_likes")
    project = models.ForeignKey(Project,
                                on_delete=models.CASCADE,
                                related_name="posts",
                                related_query_name="posts")
    view_num = models.PositiveBigIntegerField(_("views number"),
                                                 default=0)
    
    class Meta:
        db_table = "post"
        verbose_name = _("Post")
        verbose_name_plural = _("Posts")