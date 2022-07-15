from rest_framework import viewsets, mixins
from Core.models import UserSkill
from Users.serializers import UserSkillCreateSerializer

from rest_framework.exceptions import ValidationError
from django.db import IntegrityError

from rest_framework import status
from rest_framework.response import Response

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.utils.decorators import method_decorator

create_responses = {"201": openapi.Response(description="In caso di aggiunta di una o più skill riuscita",
                                            schema=openapi.Schema(type=openapi.TYPE_OBJECT,properties={})),
                    "400": openapi.Response(description="Nel caso in cui sia stata aggiunta una skilla da presente per quello user",
                                            schema=openapi.Schema(type=openapi.TYPE_OBJECT,properties={
                                                "skill":openapi.Schema(type=openapi.TYPE_STRING)}),
                                            examples={"application/json":{"skill":"è già stata abbinata questa skill a questo utente"}}),
                    "400.": openapi.Response(description="Caso in cui l'id della skill mandato non fa riferito a nessuna skill esistente",
                                            schema=openapi.Schema(type=openapi.TYPE_OBJECT,properties={
                                                "error":openapi.Schema(type=openapi.TYPE_STRING)}),
                                            examples={"application/json":{"Error":"è già stata abbinata questa skill a questo utente"}})}


@method_decorator(name="create",
                  decorator=swagger_auto_schema(responses=create_responses,
                                                request_body=UserSkillCreateSerializer(many=True)))
class UserSkillLCUDView(mixins.CreateModelMixin,
                        mixins.ListModelMixin,
                        mixins.UpdateModelMixin,
                        mixins.DestroyModelMixin,
                        viewsets.GenericViewSet):
    """
    create:
    Aggiungi una skill all'utente.
    
    Permette di aggiungere una skill con il livello all'utente che ha fatto la richiesta.
    Puoi mandare una singola skill oppure una lista di skills usando questo formato:
    [ { dati skill }, { ... }, ... ]
        
    update:
    Aggiorna i dati di una skill.  
    
    Aggiorna i dati della skill, la skill da aggiornare viene decisa in base all'id della skill messo nell'url ({skill} = id skill).
    Nel caso di un'aggiornamento parziale (PATCH) ritornano solo i campo aggiornati.
    
    partial_update:
    Aggiorna i dati di una skill.
    
    Aggiorna i dati della skill, la skill da aggiornare viene decisa in base all'id della skill messo nell'url ({skill} = id skill).
    Nel caso di un'aggiornamento parziale (PATCH) ritornano solo i campo aggiornati.
      
    destroy:
    Rimuovi una skill da un utente.
    
    Rimuovi una skill da un utente, la skill da eliminare viene decisa in base all'id della skill messo nell'url ({skill} = id skill).
    """
    serializer_class = UserSkillCreateSerializer
    queryset = UserSkill.objects.all()
    lookup_field = "skill"
    
    def get_queryset(self):
        return UserSkill.objects.filter(user=self.request.user)
    
    def create(self, request, *args, **kwargs):
        if not isinstance(request.data, list):
            return super(UserSkillLCUDView, self).create(request, *args, **kwargs)
        serializer = self.get_serializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    def perform_create(self, serializer):
        try: serializer.save(user=self.request.user)
        except IntegrityError:
            raise ValidationError({"error":"è già stata abbinata questa skill a questo utente"})
        
    def update(self, request, *args, **kwargs):
        response = super().update(request,*args,**kwargs)
        if response.status_code != 200: return response
        return Response(data=request.data,
                        status=response.status_code,
                        headers=response.headers)