from django.urls import path
import Projects.views as vw
from rest_framework.routers import DefaultRouter
    
router = DefaultRouter()
router.register(r"projects", vw.ProjectsListCreateView)
router.register(r"projects", vw.ProjectsRUDView)
router.register(r"role", vw.RoleUpdateDestroyView)
router.register(r"projects/users", vw.UserProjectUpdateDestroyView)
router.register(r"showcase", vw.ShowcaseRUDView)
router.register(r"event", vw.EventUpdateDestroyView)
router.register(r"event/task", vw.EventTaskUpdateDestroyView)
router.register(r"poll", vw.PollUpdateDestroyView)
router.register(r"poll/option", vw.PollOptionUpdateDestroyView)

urlpatterns = router.urls

urlpatterns += [
    path('user/events/', vw.EventForUserListView.as_view({"get":"list"}), name="event-for-user-list"),
    
    path('projects/<uuid:id>/roles/',vw.RoleListCreateView.as_view({"get":"list","post":"create"}),name="roles-list-create"),
    path('projects/<uuid:id>/tags/', vw.ProjectTagCreateView.as_view({'post':'create'}),name="project-tag-create"),
    path('projects/<uuid:id>/users/',vw.UserProjectListCreateView.as_view({"get":"list","post":"create"}),name="users-projects-list-create"),
    path('projects/<uuid:id>/showcases/',vw.ShowcaseListCreateView.as_view({"get":"list", "post":"create"}),name="showcases-list-create"),
    path('projects/<uuid:id>/events/', vw.EventInProjectListView.as_view({"get":"list"}), name="event-in-project-list"),
    
    path('showcase/<uuid:id>/messages/',vw.MessageListView.as_view({'get':'list'}),name="messages-list"),
    path('showcase/<uuid:id>/messages/text/',vw.TextMessageCreateView.as_view({'post':'create'}),name="text-message-create"),
    path('showcase/<uuid:id>/messages/event/',vw.EventCreateView.as_view({'post':'create'}),name="event-create"),
    path('showcase/<uuid:id>/messages/poll/',vw.PollCreateView.as_view({'post':'create'}),name="poll-create"),
    
    path('text/<uuid:id>/files/',vw.MessageFileCreateView.as_view({'post':'create'}),name="event-tasks-create"),
    path('event/<uuid:id>/tasks/',vw.EventTaskCreateView.as_view({'post':'create'}),name="event-tasks-create"),
    path('poll/<uuid:id>/options/',vw.PollOptionCreateView.as_view({'post':'create'}),name="poll-options-create"),
    path('poll/option/<uuid:id>/vote/',vw.PollOptionVotesAPIView.as_view(),name="poll-options-create"),
]

