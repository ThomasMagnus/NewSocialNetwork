from django.urls import path
from . import views

urlpatterns = [
    path('', views.chat_window, name='messages'),
    path('chats/', views.get_messages_data, name='chats')
]
