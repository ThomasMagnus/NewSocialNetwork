from django.urls import path
from . import views

urlpatterns = [
    path('', views.friend_template, name='friends')
]
