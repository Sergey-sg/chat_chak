from django.urls import path

from .views import RoomListView, RandomChuckJokes, CreateMessageView


urlpatterns = [
    path('', RoomListView.as_view(), name='rooms_list'),
    path('jokes/', RandomChuckJokes.as_view(), name='random_jokes'),
    # path('<int:pk>/create-message/', CreateMessageView.as_view(), name='create_message'),
    path('create-message/', CreateMessageView.as_view(), name='create_message'),
]
