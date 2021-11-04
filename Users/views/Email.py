from rest_framework import generics
from Users.serializers import EmailSerializer
from Core.models import Email


class EmailCreateView(generics.CreateAPIView):
    queryset = Email.objects.all()
    serializer_class = EmailSerializer
