from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from Core.models import AbstractName, Project
from django.utils import timezone
import uuid

class Role(AbstractName):
    project = models.ForeignKey(Project,
                                on_delete=models.CASCADE,
                                related_name="roles",
                                related_query_name="roles")
    
    class Meta:
        db_table = "role"
        verbose_name = _("Role")
        verbose_name_plural = _("Roles")
        
        
        

class UserProject(models.Model):
    date_added_help_text = _("Data di aggiunta utente nel progetto")
    role_help_text = _("Elenco dei ruoli dell'utente all'interno del progetto")
    
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    project = models.ForeignKey(Project,
                                on_delete=models.CASCADE)
    role = models.ManyToManyField(Role,
                                  related_name="users",
                                  related_query_name="users",
                                  help_text=role_help_text)
    date_added = models.DateTimeField(_("date added"), 
                                      default=timezone.now,
                                      help_text=date_added_help_text)
    
    class Meta:
        unique_together = (("user", "project"),)
        db_table = "user_project"
        verbose_name = _("User Project")
        verbose_name_plural = _("User Projects")
        ordering = ["-date_added"]
        indexes = [models.Index(fields=["-date_added"])]
        
    def __str__(self):
        return f"{self.project} - {self.user}"
    