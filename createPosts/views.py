from django.http import HttpResponse
from .models import Posts
from services.generate_id import generate_random_num
from django.contrib.auth.models import User
import json
import datetime


def get_post(request, id):
    return Posts.objects.get(id=id)


def post_creator(request):
    if request.method == 'POST':
        user = User.objects.get(id=request.session['sessionID'])
        data_post = request.POST.get('comment')
        posts = Posts(id=generate_random_num(), post=data_post, user_date=datetime.datetime.now(),
                      user_id=user.id, user_login=user.username)
        posts.save()
        return HttpResponse('Hello World')


def edit_post(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        Posts.objects.filter(id=data['id']).update(post=data['editPost'])
        return HttpResponse('Пост изменён!')


def delPost(request):
    if request.method == 'POST':
        data = int(json.loads(request.body)['postId'])
        Posts.objects.filter(id=data).delete()
        return HttpResponse("Пост удалён")
