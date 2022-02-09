import datetime

from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.http import HttpResponse

from authorization.models import UserFile
from createPosts.models import Posts
from .news import DataNewsCreator
from services.forms import CoverForm


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
        post = Posts.objects.filter(user_id=user_id).order_by('-user_date')
    except Posts.DoesNotExist:
        print('Нет постов')

    try:
        if request.session['userid']:
            name = f'{user.first_name} {user.last_name}'
            date = datetime.datetime.now().date()
            data_news_creator = DataNewsCreator()
            news_data = data_news_creator.create_news_data()

            cover_form = CoverForm(request.POST, request.FILES)
            cover_photo = UserFile.objects.get(id=user_id).cover_photo

            data_dict = {**data_dict, **{'name': name, 'user_id': user_id, 'user_post_dict': post, 'date': date,
                                         'news_data': news_data, 'cover_photo': cover_photo, 'cover_form': cover_form}}

            return render(request, 'user.html', data_dict)
    except Exception as ex:
        print(ex)
        return redirect(to='/')


def logout_user(request):
    logout(request)
    return redirect(to='/')


def change_cover(request):
    if request.method == 'POST':
        file = request.FILES
        print(file)
        # photo = request.FILES['file']
        # file_name = request.body.decode('utf8')

        # with open(f'media/images/{file_name}', 'wb+') as file:
        #     file.write(photo)
    return HttpResponse('Изображение получено!')
