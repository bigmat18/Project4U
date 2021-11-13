from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.sites.models import Site

from allauth.account.models import EmailAddress
from allauth.socialaccount.models import SocialAccount, SocialApp, SocialToken


admin.site.unregister(Group)

admin.site.unregister(Site)

admin.site.unregister(EmailAddress)

admin.site.unregister(SocialAccount)

admin.site.unregister(SocialApp)

admin.site.unregister(SocialToken)