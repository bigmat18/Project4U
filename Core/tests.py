from rest_framework.test import APITestCase
from Core.models import User
from rest_framework_api_key.models import APIKey


class BaseTestCase(APITestCase):
    first_name    = "prova"
    last_name     = "prova"
    email         = "prova@prova.com"
    password      = "prova1234567_"
    
    def init_test(self, auth=False):
        self.user = User.objects.create_user(password=self.password,email=self.email,
                                             first_name=self.first_name,last_name=self.last_name)
        key = APIKey.objects.create_key(name="prova")
        self.client.credentials(HTTP_X_API_KEY=key[1])
        if auth: self.client.force_authenticate(user=self.user)
        return {"first_name": self.first_name, "last_name": self.last_name,
                "email": self.email, "password": self.password}



from Users.tests.Auth import LoginRegistrationTestCase
from Users.tests.User import UsersTestCase
from Users.tests.Skill import SkillTestCase, UserSkillTestCase
from Users.tests.ExternalProject import ExternalProjectTestCase
from Users.tests.UserEducation import UserEducationTestCase

from Projects.tests.Project import ProjectsTestCase
from Projects.tests.Role import RoleTestCase