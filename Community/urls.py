from django.urls import path
from rest_framework.routers import DefaultRouter
import Community.views as vw
    
router = DefaultRouter()
router.register(r'paragraph', vw.NewsParagraphUpdateDeleteView)
router.register(r'news', vw.NewsRUDView)
router.register(r'paragraph-image', vw.NewsParagraphImageUpdateDeleteView)
router.register(r'text-post', vw.TextPostUpdateDestroyView)
router.register(r'project/question', vw.ProjectQuestionUpdateDestroyView)
router.register(r'project/answer', vw.ProjectAnswerUpdateDestroyView)
router.register(r'post/comment', vw.PostCommentUpdateDestroyView)


urlpatterns = router.urls

urlpatterns += [
    path('projects/<uuid:id>/news/',vw.NewsCreateView.as_view({"post":"create"}),name="news-create"),
    path('news/<uuid:id>/paragraphs/',vw.NewsParagraphListCreateView.as_view({"get":"list","post":"create"}),name="news-paragraphs-list-create"),
    path('paragraph/<uuid:id>/image/',vw.NewsParagraphImageCreateView.as_view({"post":"create"}),name="news-paragraphs-image-create"),
    path('projects/<uuid:id>/text-posts/', vw.TextPostCreateView.as_view({"post":"create"}), name="text-post-create"),
    path('projects/<uuid:id>/questions/',vw.ProjectQuestionCreateView.as_view({"post":"create"}), name="question-create"),
    path('question/<str:slug>/answers/',vw.ProjectAnswerCreateView.as_view({"post":"create"}), name="answer-create"),
    
    path('posts/', vw.PostListView.as_view({"get": "list"}), name="post-list"),
    path('post/<uuid:id>/comments/', vw.PostCommentListCreateView.as_view({"get": "list","post": "create"}), name="post-comment-list-create"),
    path('post/comment/<uuid:id>/likes/', vw.PostCommentLikeAPIView.as_view(), name="post-comment-likes"),
]