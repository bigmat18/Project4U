from rest_framework import viewsets, generics
from ..serializers import NewsSerializer, NewsParagraphSerializer, NewsParagraphImageSerializer
from Core.models import News, NewsParagraphImage, NewsParagraph, Project
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework import status

class NewsCreateView(generics.CreateAPIView,
                     viewsets.GenericViewSet):
    serializer_class = NewsSerializer
    queryset = News.objects.all()
    
    def create(self, request, *args, **kwargs):
        if "paragraphs" in request.data: 
            paragraphs = request.data["paragraphs"]
            del request.data["paragraphs"]
        else: paragraphs = None
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        news = self.perform_create(serializer)
        
        if paragraphs:
            if not isinstance(paragraphs, list):
                news.delete()
                return Response({"Error": "Paragraphs fields must be a list"},
                                status=status.HTTP_400_BAD_REQUEST)
                
            for index, paragraph in enumerate(paragraphs):
                if "images" in paragraph: 
                    images = paragraph['images']
                    del paragraph['images']
                else: images = None
                
                serializer_paragraph = NewsParagraphSerializer(data=paragraph)
                
                try: serializer_paragraph.is_valid(raise_exception=True)
                except Exception as e: news.delete(); raise e
                
                paragraph = serializer_paragraph.save(news=news, order_paragraph=index)
                
                if images:
                    if not isinstance(images,list):
                        news.delete()
                        return Response({"Error": "Images in paragraph fields must be a list"},
                                        status=status.HTTP_201_CREATED)
                    
                    for image in images:
                        serializer_image = NewsParagraphImageSerializer(data=image)
                        
                        try: serializer_image.is_valid(raise_exception=True)
                        except Exception as e: news.delete(); raise e
                        
                        serializer_image.save(paragraph=paragraph)
                        
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
    
    def perform_create(self, serializer):
        instance = serializer.save(author=self.request.user,
                                   project=get_object_or_404(Project, 
                                                             id=self.kwargs['id']))
        return instance


class NewsRUDView(generics.RetrieveUpdateDestroyAPIView,
                  viewsets.GenericViewSet):
    serializer_class = NewsSerializer
    queryset = News.objects.all()
    lookup_field = "id"
    
    
class NewsParagraphListCreateView(generics.ListCreateAPIView,
                                  viewsets.GenericViewSet):
    serializer_class = NewsParagraphSerializer
    queryset = NewsParagraph.objects.all()
    
    def get_queryset(self):
        return News.objects.filter(news__id=self.kwargs['id'])
    
    def perform_create(self, serializer):
        serializer.save(news=get_object_or_404(News, id=self.kwargs['id']))


class NewsParagraphUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView,
                                    viewsets.GenericViewSet):
    serializer_class = NewsParagraphSerializer
    queryset = NewsParagraph.objects.all()
    lookup_field = "id"