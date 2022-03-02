from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from Core.models import Project, AbstractCreateUpdate
from Core.models.Projects.Showcase import Showcase
from django.db.models import Q
from django.db.models.signals import pre_delete 
from django.dispatch import receiver
import uuid

class Role(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    name = models.CharField(_("name"), max_length=64)
    project = models.ForeignKey(Project,
                                on_delete=models.CASCADE,
                                related_name="roles",
                                related_query_name="roles")
    
    class Meta:
        db_table = "role"
        verbose_name = _("Role")
        verbose_name_plural = _("Roles")
        
    def __str__(self): return str(self.id)
        

class UserProject(AbstractCreateUpdate):
    __date_added_help_text = _("Data di aggiunta utente nel progetto")
    __role_help_text = _("Elenco dei ruoli dell'utente all'interno del progetto")
    
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    project = models.ForeignKey(Project,
                                on_delete=models.CASCADE)
    role = models.ManyToManyField(Role,
                                  blank=True,
                                  related_name="users",
                                  related_query_name="users",
                                  help_text=__role_help_text)
    
    created_at = models.DateTimeField(_('created at'),
                                      db_column="date_added",
                                      default=None,
                                      null=True,
                                      editable=False,
                                      help_text=__date_added_help_text)
    
    class Meta(AbstractCreateUpdate.Meta):
        unique_together = (("user", "project"),)
        db_table = "user_project"
        verbose_name = _("User Project")
        verbose_name_plural = _("User Projects")
        
    def __str__(self): return f"{self.project} - {self.user}"
    
    def save(self, *args, **kwargs):
        if self._state.adding:
            showcases = Showcase.objects.filter(project=self.project)\
                                        .filter(Q(name="Generale") | Q(name="Idee"))
            for showcase in showcases: showcase.users.add(self.user)
        return super().save(*args, **kwargs)
    
    
@receiver(pre_delete, sender=UserProject)
def delete_users_from_showcases(sender, instance, **kwargs):
    for showcase in instance.project.showcases.filter(users=instance.user):
        showcase.users.remove(instance.user)