from django.urls import path
from . import views

urlpatterns = [
    path('<slug:user_id>/', views.user_template, name='users'),
    path('', views.logout_user),
]
