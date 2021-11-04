from django.db import models 
import uuid


class Email(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(max_length=254, unique=True)
    added_at = models.DateTimeField(auto_now_add=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=150, blank=True)

    class Meta:
        verbose_name          = "Email"
        verbose_name_plural   = "Emails"
        db_table              = "email"

    def __str__(self):
        return str(self.email)