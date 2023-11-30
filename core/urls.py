from django.urls import path
from . import views

urlpatterns = [
    path('', views.index.as_view(), name='index'),
    path('discussion/start', views.DiscussionCreateView.as_view(), name="Discussion_start"),
    path('discussion/update/<uuid:pk>', views.DiscussionUpdateView.as_view(), name="Discussion_update"),
    path('discussions', views.DiscussionListView.as_view(), name="Discussions"),
    path('discussion/detail/<uuid:pk>/Message', views.MessageCreateView.as_view(), name="Message_create"),
    path('discussion/<uuid:discussion_id>/messages', views.MessageListView.as_view(), name="Message_list"),
    path('discussion/<uuid:discussion_id>/toggle-like/', views.ToggleLikeView.as_view(), name='toggle_like'),
    
]
