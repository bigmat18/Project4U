from statistics import mode
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from Core.models import Skill, AbstractFile

from ...management.scripts.generete_slug import generate_random_string, generate_slug
from django.db.models import CheckConstraint, Q
from django.db.models.functions import Now

import uuid

class UserManager(BaseUserManager):

    def _create_user(self, email, password, first_name, last_name, admin, date_birth):
        if not email: raise ValueError(_('Users must have an email address'))
        if not password: raise ValueError(_('Users must have an password address'))
        if not first_name: raise ValueError(_('Users must have an first name'))
        if not last_name: raise ValueError(_('Users must have an last name'))


        email = self.normalize_email(email)
        user = self.model(email=email)
        
        user.set_password(password)
        user.admin = admin
        user.first_name = first_name
        user.last_name = last_name
        user.date_birth = date_birth
        user.date_joined = timezone.now()
        user.secret_key = generate_random_string()
        user.slug = generate_slug(f"{user.first_name}-{user.last_name}-")
        
        user.save(using=self._db)
        return user

    def create_user(self, email, password, first_name, last_name, date_birth=None):
        return self._create_user(email, password, first_name, last_name, False, date_birth)

    def create_superuser(self, email, password, first_name, last_name, date_birth=None):
        return self._create_user(email, password, first_name, last_name, True, date_birth)


def image_path(instance,path):
    return f"users/user-{instance.id}/user-image.jpg"

class TypeUser(models.TextChoices):
    BASE = 'Base'
    VERIFIED = 'Verified'
    INNOVATOR = 'Innovator'
    
class TypeVip(models.TextChoices):
    FREE = 'FREE'
    LV1 = 'LV1'
    LV2 = 'LV2'
    LV3 = 'LV3'

class User(AbstractBaseUser, AbstractFile):
    __blocked_help_text   = "Indica se un utente è stato bloccato."
    __main_role_help_text = "Indica il ruolo principale dell'utente (32 caratteri max)"
    __description_help_text = "Descrizione dell'utente (256 caratteri max)"
    
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    email = models.EmailField(_('email address'), blank=True, unique=True)
    first_name = models.CharField(_('first name'), max_length=150, blank=True)
    last_name = models.CharField(_('last name'), max_length=150, blank=True)
    image = models.ImageField(_("image"), blank=True, null=True, upload_to=image_path)
    username = models.CharField(max_length=64,blank=True,null=True,default=None)
    
    main_role = models.CharField(_('main role'), blank=True, null=True, max_length=32,
                                 help_text=__main_role_help_text)
    
    date_birth = models.DateField(_('date birth'), null=True,blank=True)
    date_joined = models.DateTimeField(_('date joined'),null=True)

    active = models.BooleanField(_("is active"), default=True)
    blocked = models.BooleanField(_("is blocked"), default=False,
                                  help_text=__blocked_help_text)
    
    admin = models.BooleanField(_("is admin"), default=False)
    type_user = models.CharField(_("type user"), choices=TypeUser.choices, 
                                 default=TypeUser.BASE, max_length=64)
    type_vip = models.CharField(_("type vip"), choices=TypeVip.choices,
                                 default=TypeVip.FREE, max_length=64)
    
    user_saved = models.ManyToManyField("self",
                                        related_name="saved_by",
                                        related_query_name="saved_by",
                                        blank=True,)
    
    project_saved = models.ManyToManyField("Project",
                                           related_name="saved_by",
                                           related_query_name="saved_by",
                                           blank=True,)
    
    description = models.TextField(_("description"), blank=True, 
                                   null=True,max_length=256,
                                   help_text=__description_help_text)
    
    location = models.CharField(_("location"),blank=True,null=True,
                                max_length=32)
    
    skills = models.ManyToManyField(Skill,
                                    through='UserSkill',
                                    through_fields=('user','skill'),
                                    related_name="users",
                                    related_query_name="users")
    slug = models.SlugField(blank=True, editable=False, unique=True)
    secret_key = models.SlugField(_("secret key"), editable=False, 
                                  unique=True,blank=True)
    
    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    
    objects = UserManager()
    
    class Meta:
        db_table = 'user'
        verbose_name = _('User')
        verbose_name_plural = _('Users')
        constraints = [
            CheckConstraint(check=Q(date_birth__lte=Now()),name="check_user_date_birth")
        ]
    
    @property
    def full_name(self): return f"{self.first_name} {self.last_name}"
    
    @property
    def is_staff(self): return self.admin
    
    @property
    def is_active(self): return self.active
    
    def has_perm(self, perm, obj=None): return True

    def has_module_perms(self, app_label): return True        
        
    def __str__(self): return f"{self.email}"