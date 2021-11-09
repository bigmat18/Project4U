from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from Core.models import Skill, AbstractSlug
import uuid

class UserManager(BaseUserManager):

    def _create_user(self, email, password, first_name, last_name, admin):
        if not email: raise ValueError(_('Users must have an email address'))
        if not password: raise ValueError(_('Users must have an password address'))
        if not first_name: raise ValueError(_('Users must have an first name'))
        if not last_name: raise ValueError(_('Users must have an last name'))


        email   = self.normalize_email(email)
        user    = self.model(email=email)
        
        user.set_password(password)
        user.admin = admin
        user.first_name = first_name
        user.last_name = last_name
        
        user.save(using=self._db)
        return user

    def create_user(self, email, password, first_name, last_name):
        return self._create_user(email, password, first_name, last_name, False)

    def create_superuser(self, email, password, first_name, last_name):
        return self._create_user(email, password, first_name, last_name, True)


class User(AbstractBaseUser, AbstractSlug):
    blocked_help_text   = "Indica se un utente è stato bloccato."
    extra_help_text = "Le esperienze scolasti o non, extra dello user"
    highschool_help_text = "La scuola superiori frequentata"
    university_help_text = "L'università frequentata"
    
    class TypeUser(models.TextChoices):
        BASE = '01', _('Base')
        VERIFIED = '02', _('Verified')
        INNOVATOR = '03', _('Innovator')
    
    class TypeVip(models.TextChoices):
        FREE = 'FREE', _('Free')
        LV1 = 'LV1', _('Level 01')
        LV2 = 'LV2', _('Level 02')
        LV3 = 'LV3', _('Level 03')
    
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,editable=False)
    email = models.EmailField(_('email address'), blank=True, unique=True)
    first_name = models.CharField(_('first name'), max_length=150, blank=True)
    last_name = models.CharField(_('last name'), max_length=150, blank=True)
    image = models.ImageField(_("image"), blank=True, null=True)
    username = models.CharField(max_length=64,blank=True,null=True,default=None)
    
    date_birth = models.DateField(_('date birth'), null=True,blank=True)
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)

    active = models.BooleanField(_("is active"), default=True)
    blocked = models.BooleanField(_("is blocked"), default=False,
                                  help_text=blocked_help_text)
    
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
    
    highscool = models.CharField(_("highscool"), max_length=256,
                                 blank=True, null=True,
                                 help_text=highschool_help_text)
    
    university = models.CharField(_("university"), max_length=256,
                                  blank=True, null=True,
                                  help_text=university_help_text)
    
    extra = models.TextField(_("extra"), blank=True, null=True,
                             help_text=extra_help_text)
    
    skills = models.ManyToManyField(Skill,
                                    through='UserSkill',
                                    through_fields=('user','skill'),
                                    related_name="users",
                                    related_query_name="users")
    
    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    
    objects = UserManager()
    
    class Meta:
        db_table = 'user'
        verbose_name = _('User')
        verbose_name_plural = _('Users')
        constraints = [
            models.CheckConstraint(check=models.Q(date_birth__gte=timezone.now()),
                                   name="date_birth__gte")
        ]
        
    def __str__(self):
        return f"{self.email}"
    
    @property
    def full_name(self): return f"{self.first_name} {self.last_name}"
    
    @property
    def is_staff(self): return self.admin
    
    @property
    def is_active(self): return self.active
    
    def has_perm(self, perm, obj=None): return True

    def has_module_perms(self, app_label): return True
    