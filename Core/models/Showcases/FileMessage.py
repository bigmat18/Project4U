from django.db import models
from Core.models import Message
import uuid

def file_path(instace,filename):
    return f"project-{instace.message.showcase.project.id}"+\
           f"/showcase-{instace.message.showcase.id}"+\
           f"/message-{instace.message.id}/{filename}"

class FileMessage(models.Model):
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
        
    def __str__(self) -> str:
        return str(self.id)