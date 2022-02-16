from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from Core.models import User, Project
from django.test.utils import override_settings
from django.test import tag
from django.core.exceptions import ObjectDoesNotExist
from ..management.scripts.decorate_all_methods import for_all_methods


@tag('AbstractFile', 'file')
@for_all_methods(override_settings(DEBUG=True))
class AbstractFileTestCase(TestCase):
    
    def setUp(self):
        self.image = SimpleUploadedFile("test.jpg", b"")
        self.user = User.objects.create_user(email="ciao", password="ciao123456",
                                            first_name="ciao", last_name="ciao")
        self.project = Project.objects.create(name="ciao",creator=self.user,image=self.image)
        self.user.image = self.image
        self.user.save()

    def test_project_delete_queryset(self):
        projects = Project.objects.all()
        projects.delete()
        self.assertQuerysetEqual(projects, Project.objects.all())

    def test_project_delete_model(self):
        project = Project.objects.get(id=self.project.id)
        project.delete()
        with self.assertRaises(ObjectDoesNotExist):
            Project.objects.get(id=self.project.id)
            
    def test_project_save_model(self):
        project = Project.objects.get(id=self.project.id)
        project.image = None
        project.save()
        self.assertEqual(project.image,None)
        
    def test_user_delete_queryset(self):
        users = User.objects.all()
        users.delete()
        self.assertQuerysetEqual(users, User.objects.all())

    def test_user_delete_model(self):
        user = User.objects.get(id=self.user.id)
        user.delete()
        with self.assertRaises(ObjectDoesNotExist):
            User.objects.get(id=self.user.id)
            
    def test_user_save_model(self):
        user = User.objects.get(id=self.user.id)
        user.image = None
        user.save()
        self.assertEqual(user.image,None)