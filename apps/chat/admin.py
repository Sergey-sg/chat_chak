from django.contrib import admin

from .models import Message, Room


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('room', 'author', 'created', 'status',)
    search_fields = ('room', 'author',)
    list_filter = ['created', 'room']


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('name', 'created', 'private',)
    search_fields = ('name',)
    list_filter = ['created']
