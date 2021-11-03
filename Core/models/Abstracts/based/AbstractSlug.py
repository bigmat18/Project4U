from django.db import models
from django.utils.translation import gettext_lazy as _
from script.generate_slug import generate_slug

class AbstractSlug(models.Model):
    slug = models.SlugField(_("slug"),
                            unique=True,
                            null=True,
                            blank=True)
    
    class Meta:
        abstract = True
        
    def save(self, *args, **kwargs):
        if self.slug is None:
            if hasattr(self, 'title'): 
                self.slug = generate_slug(self.title)
            elif hasattr(self, 'name'):
                self.slug = generate_slug(self.name)
            else: 
                self.slug = generate_slug('')
        return super().save(*args, **kwargs)