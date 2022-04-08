from django.urls import path
from . import views

urlpatterns = [
    path('<slug:user_id>/', views.get_friend_page)
]
