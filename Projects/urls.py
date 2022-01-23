from unicodedata import name
from django.urls import path
import Projects.views as vw
from rest_framework.routers import DefaultRouter
    
router = DefaultRouter()
router.register(r"projects", vw.ProjectsListCreateView)
router.register(r"projects", vw.ProjectsRUDView)
router.register(r"role", vw.RoleUpdateDestroyView)
router.register(r"projects/users", vw.UserProjectUpdateDestroyView)

urlpatterns = router.urls

urlpatterns += [
    path('projects/<uuid:id>/roles/',vw.RoleListCreateView.as_view({"get":"list","post":"create"}),name="roles-list-create"),
    path('projects/<uuid:id>/users/',vw.UserProjectListCreateView.as_view({"get":"list","post":"create"}),name="users-projects-list-create"),
    path('projects/<uuid:id>/showcases/',vw.ShowcaseListCreateView.as_view({"get":"list","post":"create"}),name="showcases-list-create"),
    path('showcase/<uuid:id>/messages/',vw.MessageListView.as_view({'get':'list'}),name="messages-list"),
    path('showcase/<uuid:id>/messages/text/',vw.TextMessageCreateView.as_view({'post':'create'}),name="text-message-create"),
    path('projects-tags/', vw.ProjectTagListCreateView.as_view({'get':'list','post':'create'}),name="project-tag-list-create")
]

