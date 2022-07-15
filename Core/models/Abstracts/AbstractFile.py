from django.db import models
from django.db.models.fields.files import ImageFieldFile, FileField
from storages.backends.s3boto3 import S3Boto3Storage
from django.utils.translation import gettext_lazy as _
from django.conf import settings
import os


class FileNotExistsException(Exception):
    __default_message = _("Non esistono campi di tipo file nel modello")
    
    def __init__(self, message=__default_message):
        self.message = message
        super().__init__(self.message)
        
        
        
class FileManager(object):
    __storage = S3Boto3Storage()

    def get_files_name(self, model):
        files_name = []
        for field in model._meta.get_fields():
            if isinstance(field, (ImageFieldFile, FileField)):
                files_name.append(field.attname)
        if not bool(files_name): raise FileNotExistsException()
        else: return files_name   
    
    def get_pre_save_file_value(self, obj, name):
        id = obj._meta.pk.value_from_object(obj)
        obj = self.__class__.objects.get(id=id)
        return self.get_file_value(obj, name)
    
    def get_post_save_file_value(self, obj, name):
        return self.get_file_value(obj, name)
    
    def get_file_value(self, obj, name):
        return obj.__getattribute__(name)
    
    def delete_file(self,name):
        if settings.DEBUG: os.remove(f"{settings.MEDIA_ROOT}/{str(name)}")
        else: self.__storage.delete(str(name))
     
     
class AbstractFileQuerySet(models.query.QuerySet, 
                           FileManager):
    
    def delete(self):
        for model in self:
            for name in self.get_files_name(model):
                file_value = self.get_file_value(model, name)
                if file_value: self.delete_file(file_value)
        return super().delete()
     
        
class AbstractFileManager(models.Manager):
    
    def get_queryset(self):
        return AbstractFileQuerySet(self.model, 
                                    using=self._db)


class AbstractFile(models.Model, 
                   FileManager):
    objects = AbstractFileManager()

    def save(self, *args, **kwargs):
        if not self._state.adding:
            for name in self.get_files_name(self):
                pre_save_file = self.get_pre_save_file_value(self, name)
                post_save_file = self.get_post_save_file_value(self, name)
                if not post_save_file and pre_save_file:
                    self.delete_file(pre_save_file)
        return super().save(*args, **kwargs)
    
    def delete(self, *args, **kwargs):
        for name in self.get_files_name(self):
            file_value = self.get_file_value(self, name)
            if file_value: self.delete_file(file_value)
        return super().delete(*args, **kwargs)
    
    class Meta:
        abstract = True