from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from Core.models import AbstractCreateUpdate
import uuid

class AbstractComment(AbstractCreateUpdate):
    @staticmethod
    def get_author_related_name():
        return '%(app_label)s_%(class)s' + '_author'
    
    @staticmethod
    def get_likes_related_name():
        return '%(app_label)s_%(class)s' + '_likes'
       
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    author = models.ForeignKey(settings.AUTH_USER_MODEL,
                               on_delete=models.CASCADE,
                               related_name=get_author_related_name.__func__(),
                               related_query_name=get_author_related_name.__func__())
    
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                   related_name=get_likes_related_name.__func__(),
                                   related_query_name=get_likes_related_name.__func__())
    
    text = models.TextField(_("text"),
                            max_length=516,
                            null=True,blank=True)
    
    
    class Meta(AbstractCreateUpdate.Meta):
        abstract = True
    