import datetime

from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import logout
from createPosts.models import Posts
from .news import DataNewsCreator


def user_template(request, user_id):
    data_dict = {
        'links': {
            'Люди': '/',
            'Интересные публикации': '/',
            'Сообщества': '/',
        },
    }

    user = User.objects.get(id=user_id)
    post = None

    try:
        post = Posts.objects.filter(user_id=user_id)
    except Posts.DoesNotExist:
        print('Нет постов')

    try:
        if request.session['userid']:
            name = f'{user.first_name} {user.last_name}'
            date = datetime.datetime.now().date()

            data_news_creator = DataNewsCreator()
            news_data = data_news_creator.create_news_data()

            data_dict = {**data_dict, **{'name': name, 'user_id': user_id, 'user_post_dict': post, 'date': date,
                                         'news_data': news_data}}
            return render(request, 'user.html', data_dict)
    except:
        return redirect(to='/')


def logout_user(request):
    logout(request)
    return redirect(to='/')
