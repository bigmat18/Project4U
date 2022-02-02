from django.test import TestCase
from Core.models import Project, User, Showcase, ShowcaseUpdate, TextMessage
from django.test import tag


@tag('ShowcaseModel')
class ShowcaseModelTestCase(TestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(email="test@test.com", password="test123456",
                                             first_name="test", last_name="test")
        self.new_user = User.objects.create_user(email="test2@test.com", password="test123456",
                                             first_name="test", last_name="test")
        self.project = Project.objects.create(name="test", creator=self.user)
        self.showcase = Showcase.objects.create(name="test", project=self.project, creator=self.user)
    
    def test_showcase_creation(self):
        self.assertEqual(self.showcase.users\
                        .filter(id=self.user.id)\
                        .exists(), True)


    def test_showcase_update(self):
        self.showcase.creator = self.new_user
        self.showcase.save()
        self.assertEqual(self.showcase.users\
                        .filter(id=self.new_user.id)\
                        .exists(), True)

    def test_showcase_update_creation(self):
        self.showcase.color = self.showcase.description = self.showcase.name = "test1"
        self.showcase.save()
        self.assertEquals(ShowcaseUpdate.objects\
                          .filter(showcase=self.showcase).count(), 3)
        
    def test_message_creation(self):
        message = TextMessage.objects.create(text="test",author=self.user,
                                             showcase=self.showcase)
        self.assertEquals(message.viewed_by.all().count(), 1)