from django.db import models
from Core.models import Message, AbstractFile

import uuid

def file_path(instace,filename):
    return f"projects/project-{instace.message.showcase.project.id}"+\
           f"/showcase-{instace.message.showcase.id}"+\
           f"/message-{instace.message.id}/{filename}"

class MessageFile(AbstractFile):
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