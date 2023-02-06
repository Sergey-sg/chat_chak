from django.http import HttpResponseNotFound, JsonResponse
from django.urls import reverse_lazy
from django.views.generic import ListView, View, CreateView
import requests
from datetime import datetime

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

    def post(self, *args, **kwargs):
        random_joke = requests.get("https://api.chucknorris.io/jokes/random")
        data = self.request.POST
        room = Room.objects.get(pk=int(data['roomId']))
        message = Message.objects.create(room=room, content=random_joke.json()['value'])
        print(message)
        return JsonResponse({'author': False, 'content': random_joke.json()['value'], 'status': True, 'updated': datetime.now()})


class CreateMessageView(CreateView):
    model = Message
    form_class = MessageForm
    template_name = 'chat/message_form.jinja2'

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
                pk=int(self.get_form_kwargs()['data']['room']), 
                readers__in=[author],
            )
            message_form.room = room
            message_form.author = author
            message_form.content = form.cleaned_data['content']
            message_form.save()
        except Room.DoesNotExist:
            return HttpResponseNotFound({'message': 'room with this user not found', 'status': 404}) 
        return JsonResponse({'author': True, 'content': message_form.content, 'status': message_form.status, 'updated': message_form.updated})


class RoomMessagesList(View):

    def get(self, *args, **kwargs):
        messages_list = Message.objects.filter(room=self.kwargs['pk'])
        out_list = []
        for message in messages_list:
            if not message.author or self.request.user.pk != message.author.pk:
                author = False
            else:
                author = True    
            out_list.append({'author': author, 'content': message.content, 'status': message.status, 'updated': message.updated})
        return JsonResponse({'messagesList': out_list})