from django.urls import path
from rest_framework.routers import DefaultRouter
import Community.views as vw
    
router = DefaultRouter()
router.register(r'paragraph', vw.NewsParagraphUpdateDeleteView)
router.register(r'news', vw.NewsRUDView)

urlpatterns = router.urls

urlpatterns += [
    path('projects/<uuid:id>/news/',vw.NewsCreateView.as_view({"post":"create"}),name="news-create"),
    path('news/<uuid:id>/paragraphs/',vw.NewsParagraphListCreateView.as_view({"get":"list","post":"create"}),name="news-paragraphs-list-create"),
]