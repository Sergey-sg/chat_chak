from django.urls import path

from .views import RoomListView, RandomChuckJokes, CreateMessageView, RoomMessagesList


urlpatterns = [
    path('', RoomListView.as_view(), name='rooms_list'),
    path('jokes/', RandomChuckJokes.as_view(), name='random_jokes'),
    path('create-message/', CreateMessageView.as_view(), name='create_message'),
    path('<int:pk>/messages-list/', RoomMessagesList.as_view(), name='messages_list'),
]
