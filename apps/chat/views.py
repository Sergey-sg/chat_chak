from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, View, CreateView
import requests

from .forms import MessageForm
from .models import Room, Message


class RoomListView(ListView):
    template_name = 'chat/rooms.jinja2'
    # model = Room
    
    def get_queryset(self):
        if self.request.user.is_authenticated:
            rooms_for_user =  Room.objects.filter(readers__in=[self.request.user])
            return rooms_for_user    
        else: 
            return []    


class RandomChuckJokes(View):

    def get(self, *args, **kwargs):
        random_joke = requests.get("https://api.chucknorris.io/jokes/random")
        return JsonResponse({'answer': random_joke.json()['value']})


class CreateMessageView(CreateView):
    model = Message
    form_class = MessageForm

    def post(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form, *args, **kwargs):
        """saves the form and return status"""
        author = self.request.user
        message_form = form.save(commit=False)
        try:
            room = Room.objects.get(
                # pk=kwargs['pk'], readers__in=[author],
                pk=1, readers__in=[author],
            )
            message_form.room = room
            message_form.author = author
            message_form.content = form.cleaned_data['content']
            message_form.save()
        except Room.DoesNotExist:
            return JsonResponse({'message': 'room with this user not found', 'status': 404}) 
        return JsonResponse({'status': 200})
