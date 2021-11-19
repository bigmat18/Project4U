from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from Core.models import User
import datetime
from rest_auth.registration.serializers import RegisterSerializer
from rest_auth.serializers import LoginSerializer

AGE = 16


class CustomLoginSerializer(LoginSerializer):
    username = None



class UserRegistrationSerializer(RegisterSerializer):
    username = None
    first_name = serializers.CharField(required=True, max_length=30)
    last_name = serializers.CharField(required=True, max_length=150)
    date_birth = serializers.DateField(required=True)
    location = serializers.CharField(required=False)
    
    def validate_date_birth(self, date_birth):
        if (datetime.date.today() - date_birth).days < AGE * 356:
            raise serializers.ValidationError(
                _(f"Per pottersi registrare è necessario aver almeno {AGE} anni"))
        return date_birth
    
    def get_cleaned_data(self):
        return {
            'first_name': self.validated_data.get('first_name'),
            'last_name': self.validated_data.get('last_name'),
            'password': self.validated_data.get('password1'),
            'email': self.validated_data.get('email'),
            'date_birth': self.validated_data.get('date_birth')
        }

    def save(self, request):
        self.cleaned_data = self.get_cleaned_data()
        user = User.objects.create_user(**self.cleaned_data)
        return user
