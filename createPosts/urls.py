from django.urls import path
from . import views

urlpatterns = [
    path('', views.post_creator),
    path('edit/', views.edit_post),
    path('deletePost/', views.delPost),
]
