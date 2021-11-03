from django.core.management.base import BaseCommand
from Core.models import User


class Command(BaseCommand):

    def handle(self, *args, **options):
        if not User.objects.filter(email="admin@admin.com").exists():
            User.objects.create_superuser("admin@admin.com", "admin123456", "admin", "admin")