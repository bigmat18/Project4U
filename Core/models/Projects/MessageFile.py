from django.db import models
from django.conf import settings
from Core.models import Message

from django.dispatch import receiver
from django.db.models.signals import pre_delete
from storages.backends.s3boto3 import S3Boto3Storage

import uuid

def file_path(instace,filename):
    return f"projects/project-{instace.message.showcase.project.id}"+\
           f"/showcase-{instace.message.showcase.id}"+\
           f"/message-{instace.message.id}/{filename}"

class MessageFile(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    message = models.ForeignKey(Message,
                                on_delete=models.CASCADE,
                                related_name="files",
                                related_query_name="files")
    file = models.FileField(upload_to=file_path,
                            max_length=1000)
    
    class Meta:
        db_table = "message_file"
        verbose_name = "MessageFile"
        verbose_name_plural = "MessageFiles"
        
    def __str__(self): return str(self.id)
    
    
if not settings.DEBUG:
    @receiver(pre_delete,sender=MessageFile)
    def pre_delete_file(sender, instance, *args, **kwargs):
        if instance.file:
            storage = S3Boto3Storage()
            storage.delete(str(instance.file))