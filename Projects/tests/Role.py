from django.http import request, response
from Core.models import Project, User, Role
from Core.tests import BaseTestCase
from rest_framework import status


class RoleTestCase(BaseTestCase):
    
    def setUp(self):
        self.init_test(True)
        self.project = Project.objects.create(name="test",creator=self.user)
        self.role1 = Role.objects.create(name="role1", project=self.project)
        
    def test_role_list(self):
        response = self.client.get(f"/api/projects/{self.project.id}/roles/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)