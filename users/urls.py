from django.urls import path
from . import views

urlpatterns = [
    path('<slug:user_id>/', views.user_template, name='users'),
    path('', views.logout_user),
    path('friends/searchFriend/', views.search_friends),
    path('changeCover/photo', views.change_cover),
    path('changeAvatar/photo', views.change_avatar),
    path('changeAvatar/buffer', views.buffer_zone),
    path('changeAvatar/buffer/del', views.del_buffer),
]
