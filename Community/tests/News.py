from Core.tests import BaseTestCase
from rest_framework import status
from django.test import tag
from django.core.files.uploadedfile import SimpleUploadedFile

@tag('Community', 'news-tests')
class NewsTestCase(BaseTestCase):
    
    def setUp(self):
        self.baseSetup()