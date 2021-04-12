from django.urls import path
from . import views


app_name = 'chat'

urlpatterns = [
    path('room/', views.course_chat_room, name='chat_room'),
]