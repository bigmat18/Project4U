from rest_framework import generics, viewsets
from Users.serializers import EmailSerializer
from Core.models import Email
from rest_framework_api_key.permissions import HasAPIKey
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.utils.decorators import method_decorator

email_400 = openapi.Response(description="Email già salvata",
                             schema=openapi.Schema(type=openapi.TYPE_OBJECT,
                                                   properties={"email":openapi.Schema(description="Email con questo email esiste già.",
                                                                                      type=openapi.TYPE_STRING)}))

@method_decorator(name="create", 
                  decorator=swagger_auto_schema(
                            operation_summary="Aggiungi una email alla mail-list",
                            operation_description="Aggiungi una email, insieme a nome (first-name) e cognome (last_name), alla mail-list",
                            responses={400:email_400}))
class EmailCreateView(generics.CreateAPIView,
                      viewsets.GenericViewSet):
    queryset = Email.objects.all()
    serializer_class = EmailSerializer
    permission_classes = [HasAPIKey]
