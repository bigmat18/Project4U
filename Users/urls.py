from django.urls import path
import Users.views as vw
from rest_framework.routers import DefaultRouter
    
router = DefaultRouter()
router.register(r'users', vw.UsersRetriveView)
router.register(r'users', vw.UsersListView)
router.register(r'skills', vw.SkillListView)
router.register(r'user/skills', vw.UserSkillLCUDView)
router.register(r'user/external-projects', vw.ExternalProjectLCUDView)
router.register(r'user/educations', vw.UserEducationLCUDView)
router.register(r'email', vw.EmailCreateView)
router.register(r'user/projects', vw.UserProjectsListView)

urlpatterns = router.urls

urlpatterns += [
    path('user/image/', vw.UserImageAPIView.as_view(), name="user-image"),
    path('user/', vw.UserRetrieveUpdateView.as_view({"get":"get","put":"put","patch":"patch"}), name="user-details"),
    path('user/info/', vw.UserInfoView.as_view(), name="user-info"),
    
    path('users/<slug:slug>/educations/', vw.UsersEducationsListView.as_view({'get':'list'}), name="users-educations"),
    path('users/<slug:slug>/skills/', vw.UsersSkillsListView.as_view({'get':'list'}), name="users-skills"),
    path('users/<slug:slug>/external-projects/', vw.UsersExternalProjectsListView.as_view({'get':'list'}), name="users-external-projects"),
]