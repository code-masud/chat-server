from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']
    ordering = ['name']
    list_filter = ['name']

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['room__name', 'user__username', 'content']
    search_fields = ['room__name', 'user__username', 'content']
    ordering = ['room__name', 'timestamp']
    list_filter = ['room__name', 'user__username', 'content']