from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from .models import Posts
from services.generate_id import generate_random_num
from django.contrib.auth.models import User
import datetime


def post_creator(request):
    if request.method == 'POST':
        user = User.objects.get(id=request.session['userid'])
        data_post = request.POST.get('comment')
        posts = Posts(id=generate_random_num(), post=data_post, user_date=datetime.datetime.now(),
                      user_id=user.id, user_login=user.username)
        posts.save()
        return HttpResponse('Hello World')
