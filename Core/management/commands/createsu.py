from django.core.management.base import BaseCommand
from Core.models import User


class Command(BaseCommand):

    def handle(self, *args, **options):
        if not User.objects.filter(email="project4u@gmail.com").exists():
            User.objects.create_superuser("project4u@gmail.com", "project4U_", "admin", "admin")