from rest_framework import serializers

from Core.models import User

from allauth.account import app_settings as allauth_settings
from allauth.account.adapter import get_adapter
from allauth.utils import email_address_exists
from django.utils.translation import gettext_lazy as _




class UserRegistrationSerializer(serializers.Serializer):
    email         = serializers.EmailField(max_length=254, 
                    required=allauth_settings.EMAIL_REQUIRED)

    first_name    = serializers.CharField(required=True, max_length=30)
    last_name     = serializers.CharField(required=True, max_length=150)
    password1     = serializers.CharField(write_only=True)
    password2     = serializers.CharField(write_only=True)

    def validate_email(self, email):
        email = get_adapter().clean_email(email)
        if allauth_settings.UNIQUE_EMAIL:
            if email and email_address_exists(email):
                raise serializers.ValidationError(
                    _("A user is already registered "
                    "with this e-mail address."))
        return email

    def validate_password(self, password):
        return get_adapter().clean_password(password)

    def validate_passwords(self, data):
        if data['password1'] != data['password2']:
            raise serializers.ValidationError(_(
            "Le password inserite sono diverse"))
        return data

    def get_cleaned_data(self):
        return {
            'first_name': self.validated_data.get('first_name'),
            'last_name': self.validated_data.get('last_name'),
            'password': self.validated_data.get('password1'),
            'email': self.validated_data.get('email')
        }

    def save(self, request):
        self.cleaned_data = self.get_cleaned_data()
        user = User.objects.create_user(**self.cleaned_data)
        return user
