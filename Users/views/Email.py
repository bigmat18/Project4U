from rest_framework import generics
from Users.serializers import EmailSerializer
from Core.models import Email
from rest_framework_api_key.permissions import HasAPIKey


class EmailCreateView(generics.CreateAPIView):
    queryset = Email.objects.all()
    serializer_class = EmailSerializer
    permission_classes = [HasAPIKey]
