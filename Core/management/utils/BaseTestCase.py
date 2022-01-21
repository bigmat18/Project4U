from rest_framework.test import APITestCase
from Core.models import User
from rest_framework_api_key.models import APIKey


class BaseTestCase(APITestCase):
    first_name    = "prova"
    last_name     = "prova"
    email         = "prova@prova.com"
    password      = "prova1234567_"
    
    def baseSetup(self):
        self.user = User.objects.create_user(password=self.password,email=self.email,
                                             first_name=self.first_name,last_name=self.last_name)
        self.new_user = User.objects.create_user(email=f"2{self.email}", password=self.email,
                                            first_name=self.first_name, last_name=self.last_name)
        key = APIKey.objects.create_key(name="prova")
        self.client.credentials(HTTP_X_API_KEY=key[1])
        self.client.force_authenticate(user=self.user)
        return {"first_name": self.first_name, "last_name": self.last_name,
                "email": self.email, "password": self.password}
