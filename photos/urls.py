from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_photos),
    path('allPhoto/', views.get_all_photos),
    path('addPhoto/', views.add_photo),
    path('delPhoto/', views.remove_photo),
]
