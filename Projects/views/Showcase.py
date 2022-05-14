from Projects.serializers import (ShowcaseReadSerializer, 
                                  ShowcaseWriteSerializer, 
                                  CustomShowcaseSerializer,
                                  MessageSerializer,
                                  UsersShowcaseSerializer)
from rest_framework import generics, viewsets
from rest_framework.views import APIView
from Core.models import Showcase, Project, UserProject, Message, User
from rest_access_policy import AccessPolicy
from rest_framework.permissions import IsAuthenticated
from rest_framework_api_key.permissions import HasAPIKey
from django.conf import settings
from django.db.models import Q
from rest_framework.response import Response
from rest_framework import status


class ShowcaseAccessPolicy(AccessPolicy):
    statements = [
        {
            "action": ["list","create"],
            "principal": "*",
            "effect": "allow",
            "condition": "is_inside_project"
        },
        {
            "action": ["retrieve","get"],
            "principal": "*",
            "effect": "allow",
            "condition": ["is_inside_showcase", "is_creator"]
        },
        {
            "action": ["update","partial_update","destroy"],
            "principal": "*",
            "effect": "allow",
            "condition": "is_creator"
        }
    ]
    
    def is_creator(self, request, view, action) -> bool:
        showcase = view.get_object()
        return request.user == showcase.creator or request.user == showcase.project.creator
    
    def is_inside_project(self, request, view, action) -> bool:
        project = generics.get_object_or_404(Project, id=view.kwargs['id'])
        return (request.user == project.creator or 
                project.users.filter(id=request.user.id).exists())
        
    def is_inside_showcase(self, request, view, action) -> bool:
        showcase = view.get_object()
        return (request.user == showcase.creator or 
                showcase.users.filter(id=request.user.id).exists())



class ShowcaseListCreateView(generics.ListCreateAPIView,
                             viewsets.GenericViewSet):
    """
    list:
    Visualizza la lista delle bacheche.
    
    Visualizza una lista di tutte le bacheche del progetto di cui è stato passato l'id.
    Soltato i partecipanti del progetto possono vedere le bacheche.
    
    create:
    Crea una nuova bacheca.
    
    Crea una nuova bacheca nel progetto di cui è stato passato l'id.
    Soltato i partecipanti del progetto possono creare delle bacheche.
    """
    queryset = Showcase.objects.all()
    permission_classes = [IsAuthenticated, ShowcaseAccessPolicy]
    if not settings.DEBUG: permission_classes.append(HasAPIKey)
    
    def get_serializer_class(self, *args, **kwargs):
        if self.action == "list":
            return ShowcaseReadSerializer
        if self.action == "create":
            return ShowcaseWriteSerializer
    
    def get_project(self):
        project_id = self.kwargs['id']
        return generics.get_object_or_404(Project, id=project_id)
    
    def get_queryset(self):
        user = self.request.user
        return Showcase.objects.filter(Q(project__id=self.kwargs['id']) & Q(users=user))\
                               .order_by("created_at")
                               
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = CustomShowcaseSerializer(queryset,request,many=True)
        return Response(serializer.data)
                               
    def create(self, request, *args, **kwargs):
        if "users" in self.request.data:
            for user in dict(self.request.data)['users']:
                if not UserProject.objects.filter(Q(project__id=self.kwargs['id']) & Q(user=user)).exists():
                    return Response(status=status.HTTP_400_BAD_REQUEST, 
                                    data={"Error":"Uno o più utenti non fanno parte del progetto"})
        return super().create(request, *args, **kwargs)
    
    def perform_create(self, serializer):
        instance = serializer.save(project=self.get_project(),
                                   creator=self.request.user)
        instance.users.add(self.request.user)
        
        
        
class ShowcaseRUDView(generics.RetrieveUpdateDestroyAPIView,
                      viewsets.GenericViewSet):
    """
    retrieve:
    Vedi i dati della bacheca.
    
    Vedi tutti i dati della bacheca di cui è stato passato l'id.
    Soltato chi è all'interno della bacheca o il creatore del progetto può vedere 
    questi dati. Endpoints da usare per esempio nella sezione dettagli del progetto.
    
    update:
    Aggiorna i dati di una bacheca.
    
    Aggiorna i dati della bacheca di cui è stato passato l'id, soltato il creatore della bacheca
    o il creatore del progetto può aggiornare i dati della bacheca.
    Endpoints da usare per esempio nella sezione dettagli del progetto per modificare i dati.
    
    partial_update:
    Aggiorna i dati di una bacheca.
    
    Aggiorna i dati della bacheca di cui è stato passato l'id, soltato il creatore della bacheca
    o il creatore del progetto può aggiornare i dati della bacheca.
    Endpoints da usare per esempio nella sezione dettagli del progetto per modificare i dati.
    
    destroy:
    Elimana una bacheca.
    
    Elimna la bacheca di cui è stato passato l'id, soltato il creatore della bacheca
    o il creatore del progetto può eliminare la bacheca.
    """
    queryset = Showcase.objects.all()
    lookup_field = "id"
    permission_classes = [IsAuthenticated, ShowcaseAccessPolicy]
    if not settings.DEBUG: permission_classes.append(HasAPIKey)
    
    def get_serializer_class(self, *args, **kwargs):
        if self.action == "retrieve" or self.action == "destroy":
            return ShowcaseReadSerializer
        if self.action == "update" or self.action == "partial_update":
            return ShowcaseWriteSerializer
        
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = CustomShowcaseSerializer(instance=instance,request=request)
        return Response(serializer.data)
        
    def update(self, request, *args, **kwargs):
        response = self.check_users_in_project(request)
        if response is not None and response.status_code  == status.HTTP_400_BAD_REQUEST: return response
        return super().update(request, *args, **kwargs)
    
    def partial_update(self, request, *args, **kwargs):
        response = self.check_users_in_project(request)
        if response is not None and response.status_code  == status.HTTP_400_BAD_REQUEST: return response
        return super().partial_update(request, *args, **kwargs)
    
    def check_users_in_project(self, request):
        if "users" in request.data:
            for user in dict(request.data)['users']:
                if not UserProject.objects.filter(Q(project__id=self.kwargs['id']) & Q(user=user)).exists():
                    return Response(status=status.HTTP_400_BAD_REQUEST, 
                                    data={"Error":"Uno o più utenti non fanno parte del progetto"})
    
    def perform_update(self, serializer):
        instance = serializer.save()
        self.add_creator_to_users(instance)

    def add_creator_to_users(self, instance):
        if not instance.users.filter(id=instance.creator.id).exists():
            instance.users.add(instance.creator)
     


class ShowcaseBaseAPIView(viewsets.GenericViewSet,
                          APIView):
    permission_classes = [IsAuthenticated, ShowcaseAccessPolicy]
    if not settings.DEBUG: permission_classes.append(HasAPIKey)
    
    def get_object(self):
        id = self.kwargs['id']
        return Showcase.objects.get(id=id)    
            
      
            
class ShowcaseLastMessageAPIView(ShowcaseBaseAPIView):
    """
    get:
    Ritorna ultimo messaggio.
    
    Ritorna l'utlimo messaggio della showcase.
    """
    
    def get(self, request, id):
        message = Message.objects.filter(Q(showcase=self.get_object()) & ~Q(type_message="EVENT"))\
                                 .select_related("author")\
                                 .order_by('updated_at')\
                                 .first()
        return Response(data=MessageSerializer(message).data, status=status.HTTP_200_OK)
    
    
    
class ShowcaseLastEventAPIView(ShowcaseBaseAPIView):
    """
    get:
    Ritorna ultimo evento.
    
    Ritorna l'ultimo evento della showcase.
    """
    
    def get(self, request, id):
        message = Message.objects.filter(Q(showcase=self.get_object()) & Q(type_message="EVENT"))\
                                 .select_related("author")\
                                 .order_by('updated_at')\
                                 .first()
        return Response(data=MessageSerializer(message).data, status=status.HTTP_200_OK)
    
    
    
class ShowcaseNotifyAPIView(ShowcaseBaseAPIView):
    """
    get:
    Ritorna notifiche non lette.
    
    Ritorna il numero di notifiche non lette dall'utente che ha effettuato la richiesta.
    """
    
    def get(self, request, id):
        notify = Message.objects.filter(showcase=self.get_object())\
                              .exclude(viewed_by=self.request.user)\
                              .count()
        return Response(data={"notify": notify}, status=status.HTTP_200_OK)
    
    
    
class ShowcaseUsersAPIView(ShowcaseBaseAPIView):
    """
    get:
    Ritorna lista utenti.
    
    Ritorna la lista degli utenti all'interno della showcase.
    """
    
    def get(self,request, id):
        users = User.objects.filter(showcases=self.get_object())
        return Response(data={"users": UsersShowcaseSerializer(users, many=True).data}, 
                        status=status.HTTP_200_OK)