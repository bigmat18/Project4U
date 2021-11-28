from django.urls import path
import Users.views as vw
from rest_framework.routers import DefaultRouter
    
router = DefaultRouter()
router.register(r'users', vw.UserRetriveView)
router.register(r'users', vw.UserListView)
router.register(r'skills', vw.SkillListView)
router.register(r'user/skills', vw.UserSkillCUDView)
router.register(r'user/external-projects', vw.ExternalProjectCUDView)
router.register(r'user/educations', vw.UserEducationCUDView)
router.register(r'email', vw.EmailCreateView)

urlpatterns = router.urls

urlpatterns += [
    path('user/image/', vw.UserImageView.as_view(), name="user-image"),
    path('user/', vw.CustumUserDetailsView.as_view({'put':'update','patch':'update','get':'retrieve'}), name="user-detail"),
]