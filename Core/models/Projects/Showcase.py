from django.db import IntegrityError, models
from django.utils.translation import gettext_lazy as _
from Core.models import AbstractCreateUpdate
from .ShowcaseUpdate import ShowcaseUpdate
from django.conf import settings
import uuid


class Showcase(AbstractCreateUpdate):
    __default_help_text = _("Indica se una bacheca è default o meno")
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    name = models.CharField(_("name"),max_length=64)
    description = models.TextField(_("description"),max_length=516,null=True,blank=True)
    color = models.CharField(max_length=16, blank=True, null=True)
    default = models.BooleanField(default=False,help_text=__default_help_text)
    project = models.ForeignKey("Project",
                                on_delete=models.CASCADE,
                                related_name="showcases",
                                related_query_name="showcases")
    users = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                   related_name="showcases",
                                   related_query_name="showcases",
                                   blank=True)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL,
                                on_delete=models.SET_NULL,
                                null=True,
                                related_name="showcases_created",
                                related_query_name="showcases_created")
    
    class Meta:
        db_table = "showcase"
        verbose_name = _("Showcase")
        verbose_name_plural = _("Showcases")
        
        
    def save(self,*args, **kwargs):
        self.check_creator_inside_project()
        if not self._state.adding: self.check_showcase_update()
        showcase = super().save(*args,**kwargs)
        self.setup_creator()
        return showcase
    
    def check_creator_inside_project(self):
        if (not self.project.users.filter(id=self.creator.id).exists()
            and not self.default and self.project.creator != self.creator):
            raise IntegrityError("Il creatore della bacheca deve far parte del progetto")
            
    def check_showcase_update(self):
        pre_save_showcase = Showcase.objects.get(id=self.id)
        if pre_save_showcase.description != self.description:
            self.create_showcase_update("DESC")
        if pre_save_showcase.color != self.color:
            self.create_showcase_update("COLOR")
        if pre_save_showcase.name != self.name:
            self.create_showcase_update("NAME")
            
            
    def create_showcase_update(self, type_update):
        update = ShowcaseUpdate.objects.create(author=self.creator,showcase=self,
                                               type_update=type_update,type_message="UPDATE")
        update.viewed_by.add(self.creator)
        
        
    def setup_creator(self):
        if not self.users.filter(id=self.creator.id).exists():
            self.users.add(self.creator)
      
        
    def __str__(self): return f"{self.project}-{self.name}"
