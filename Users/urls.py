from django.urls import path
import Users.views as vw
from rest_framework.routers import DefaultRouter

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
    
    
router = DefaultRouter()
router.register(r'users', vw.UserRetriveView)
router.register(r'users', vw.UserListView)
router.register(r'skills', vw.SkillListView)
router.register(r'user/skills', vw.UserSkillCUDView)
router.register(r'user/external-projects', vw.ExternalProjectCUDView)
router.register(r'user/educations', vw.UserEducationCUDView)

urlpatterns = router.urls

#--------------- EMAIL DOC ------------
email_400 = openapi.Response(description="Email già salvata",
                           schema=openapi.Schema(type=openapi.TYPE_OBJECT,
                                                properties={"email":openapi.Schema(description="Email con questo email esiste già.",
                                                                                             type=openapi.TYPE_STRING)}))

email_schema_view = \
   swagger_auto_schema(method='post',
                       operation_summary="Aggiungi una email alla mail-list",
                       operation_description="Aggiungi una email, insieme a nome (first-name) e cognome(last_name), alla mail-list",
                       responses={400:email_400})(vw.EmailCreateView.as_view())
#--------------- EMAIL DOC ------------


urlpatterns += [
    path('email/', email_schema_view, name="email-create"),
    path('user/image/', vw.UserImageView.as_view(), name="user-image"),
    path('user/', vw.CustumUserDetailsView.as_view({'put':'update',
                                                    'patch':'update',
                                                    'get':'retrieve'}), name="user-detail"),
]