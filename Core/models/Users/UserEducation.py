from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.db.models import CheckConstraint, Q, F
import uuid

class UserEducation(models.Model):
    
    class TypeEducation(models.TextChoices):
        UNIVERSITY = 'University'
        HIGHSCHOOL = 'Highschool'
        MASTER = 'Master'
        COURSE = 'Course'
        DOCTORATE = 'Doctorate'
        OTHER = 'Other'
    
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    type = models.CharField(max_length=32,choices=TypeEducation.choices,
                            default=TypeEducation.OTHER)
    description = models.TextField(_("description"),max_length=516,null=True,blank=True)

    started_at = models.DateField()
    ended_at = models.DateField(null=True,blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE,
                             related_name="educations",
                             related_query_name="educations")
    
    
    class Meta:
        ordering = ['started_at']
        db_table = "user_education"
        verbose_name = _("User Education")
        verbose_name_plural = _("User Educations")
        constraints = [
            CheckConstraint(check=Q(ended_at__gt=F('started_at')),
                            name="check_user_education_start_date")
        ]
        
    def __str__(self): return str(self.id)
