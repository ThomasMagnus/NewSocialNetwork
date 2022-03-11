from django.urls import path
from . import views

urlpatterns = [
    path('<slug:user_id>/', views.user_template, name='users'),
    path('', views.logout_user),
    path('changeCover/photo', views.change_cover),
    path('friends/searchFriend/', views.search_friends)
]
