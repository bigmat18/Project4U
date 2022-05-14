from django.shortcuts import get_object_or_404
from rest_framework import generics, viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from Users.serializers import (UsersDetailsSerializer, 
                               UsersListSerializer,
                               CurrentUserInfoSerializer, 
                               CurrentUserImageSerializer,
                               ExternalProjectSerializer,
                               UserSkillListSerializer,
                               UserEducationSerializer)
from Projects.serializers import ProjectListSerializer
from rest_auth.views import UserDetailsView
from Core.models import User, Project, ExternalProject, UserEducation, UserSkill

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.utils.decorators import method_decorator
from django.db.models import OuterRef, Subquery, Prefetch, Q, Value, IntegerField
import django_filters as filters



class UserFilter(filters.FilterSet):
    skills = filters.CharFilter(method='get_skills')
    
    class Meta:
        model = User
        fields = ["skills"]
        
    def get_skills(self, queryset, name, value):
        queryset = queryset.annotate(similarity=Value(0, output_field=IntegerField()))
        for skill in dict(self.data)['skills']:
            skill = skill.split(',')
            queryset = queryset.filter(Q(skills__id=skill[0]) & 
                                       Q(user_skill__level__gte=skill[1]) & 
                                       Q(user_skill__level__lte=skill[2]))
        return queryset



class UserRetrieveUpdateView(UserDetailsView,
                             viewsets.GenericViewSet):    
    """
    get:
    Recupera i dati dell'utente loggato.
    
    Recupera i dati dell'utente attualmente loggato, quindi i dati che vengono visti sono quelli di 
    chi ha fatto la richiesa.
    
    put:
    Aggiorna i dati dell'utente loggato.
    
    Aggiorna (PUT, PATCH) i dati dell'utente loggato, cioè di quello che ha fatto la richiesta. 
    E' possibili aggiornare si in modo parziale (PATCH) che totale (PUT). Ritorna solo i dati aggiornati.
    ------ Anche se non mostrato è possibili aggiornare l'immagine profilo ------
    
    patch:
    Aggiorna i dati dell'utente loggato
    
    Aggiorna (PUT, PATCH) i dati dell'utente loggato, cioè di quello che ha fatto la richiesta. 
    E' possibili aggiornare si in modo parziale (PATCH) che totale (PUT). Ritorna solo i dati aggiornati.
    ------ Anche se non mostrato è possibili aggiornare l'immagine profilo ------
    """
    
    def put(self, request, *args, **kwargs):
        response = self.update(request, *args, **kwargs)
        if response.status_code != 200: return response
        if "image" in request.data: request.data['image'] = response.data['image']
        return Response(data=request.data,
                        status=response.status_code,
                        headers=response.headers)
    
    def patch(self, request, *args, **kwargs):
        response = self.partial_update(request, *args, **kwargs)
        if response.status_code != 200: return response
        if "image" in request.data: request.data['image'] = response.data['image']
        return Response(data=request.data,
                        status=response.status_code,
                        headers=response.headers)



class UsersListView(generics.ListAPIView,
                   viewsets.GenericViewSet):

    """
    list:
    Ritorna la lista di tutti gli utente.

    Ritorna una lista di tutti gli utente salvati nel DB in un formato ridotto. E' necessario
    essere autenticati per ricere una risposta. Questo endpotins servità quando ci sarà
    la sezione dedica alla ricerca di persone da aggiungere a progetti.
    E' possibile filtrare gli utenti per una o più skills aggiungendo in fondo all'url '?skills=id,lv-min,lv-ax' dove al
    posto di id si inserisce l'id di una skill, al posto di lv-min il livello minimo che deve avere l'utente e al posto di lv-max
    il livello massimo. E' possibile inoltre filtrare per più skills in questo caso inserire nell'url '?skills=id,lv-min,lv-ax&skills=id,lv-min,lv-max&...' 
    """
    serializer_class = UsersListSerializer
    filterset_class = UserFilter
    queryset = User.objects.filter(active=True)
    
    def get_queryset(self):
        query = Subquery(UserSkill.objects.filter(user_id=OuterRef("user_id")).order_by('-level').values_list('pk')[:3])
        return User.objects.filter(Q(active=True) & Q(blocked=False))\
                           .prefetch_related(Prefetch('user_skill', queryset=UserSkill.objects.filter(pk__in=query)\
                                                                                              .select_related('skill')
                                                                                              .order_by('-level')))


class UsersRetriveView(generics.RetrieveAPIView,
                      viewsets.GenericViewSet):
    """
    retrieve:
    Ristituisce i dettagli di un'utente.

    Ritorna tutti i dettagli di un utente di cui è stato passato la slug nell'url.
    Serve quando si entra per esempio nel profilo di un'utente
    """
    serializer_class = UsersDetailsSerializer
    queryset = User.objects.filter(active=True)
    lookup_field = "slug"



@method_decorator(name="get",decorator=swagger_auto_schema(
                             responses={"200":CurrentUserImageSerializer}))
class UserInfoView(APIView):
    
    def get(self, request, *args, **kwargs):
        """
        Restituisce dati utente loggato.
        
        Restituisce dati dell'utente loggato (cioè di quello che ha fatto la richesta) in un formato ridotto.
        Questo endpoints serve per inserire i dati in picoli paragrafi come la navbar del sito o un'ateprima dell'account
        quando l'utente naviga per l'app.
        """
        user = get_object_or_404(User, id=request.user.id)
        serializer = CurrentUserInfoSerializer(instance=user)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
  
    
    
@method_decorator(name="get",decorator=swagger_auto_schema(
                             responses={"200":openapi.Schema(type=openapi.TYPE_OBJECT,
                                                            properties={"image":openapi.Schema(
                                                                        type=openapi.TYPE_STRING)})}))
class UserImageAPIView(APIView):

    def get(self, request, *args, **kwargs):
        """
        Restituisce l'immage dell'utente loggato.
        
        Restituisce solo l'immage dell'utente loggato (cioè di quello che ha fatto la richesta).
        Endpoints da utilizzare per l'ateprima dell'immage dell'utente per esempio in una navbar.
        """
        user = User.objects.get(id=request.user.id)
        serializer = CurrentUserImageSerializer(user)
        return Response(status=status.HTTP_200_OK,data=serializer.data)
    
    

class UserProjectsListView(generics.ListAPIView,
                           viewsets.GenericViewSet):
    """
    list:
    Vedi la lista dei progetti dell'utente loggato.
    
    Vedi la lista dei progetti dell'utente loggato (cioè di quello che fa la richiesta), i progetti
    che vede sono quelli o che ha creato o che è dentro come partecipante.
    """
    serializer_class = ProjectListSerializer
    queryset = Project.objects.all()
    
    def get_queryset(self):
        return Project.objects.filter(users=self.request.user.id)
    
    
class UsersExternalProjectsListView(generics.ListAPIView,
                                    viewsets.GenericViewSet):
    serializer_class = ExternalProjectSerializer
    
    def get_queryset(self):
        slug = self.kwargs['slug']
        return ExternalProject.objects.filter(user__slug=slug)


class UsersEducationsListView(generics.ListAPIView,
                              viewsets.GenericViewSet):
    serializer_class = UserEducationSerializer
    
    def get_queryset(self):
        slug = self.kwargs['slug']
        return UserEducation.objects.filter(user__slug=slug)


class UsersSkillsListView(generics.ListAPIView,
                          viewsets.GenericViewSet):
    serializer_class = UserSkillListSerializer
    
    def get_queryset(self):
        slug = self.kwargs['slug']
        return UserSkill.objects.filter(user__slug=slug)