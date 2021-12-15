from django.db import models
from Core.models import AbstractText
from django.conf import settings
from django.utils.translation import gettext_lazy as _
import uuid

class TypeEducation(models.TextChoices):
        UNIVERSITY = 'University'
        HIGHSCHOOL = 'Highschool'
        MASTER = 'Master'
        COURSE = 'Course'
        DOCTORATE = 'Doctorate'
        OTHER = 'Other'

class UserEducation(AbstractText):
    
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    type = models.CharField(max_length=32,choices=TypeEducation.choices,
                            default=TypeEducation.OTHER)
    started_at = models.DateField()
    ended_at = models.DateField(null=True,blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE,
                             related_name="educations",
                             related_query_name="educations")
    
    
    class Meta:
        db_table = "user_education"
        verbose_name = _("User Education")
        verbose_name_plural = _("User Educations")