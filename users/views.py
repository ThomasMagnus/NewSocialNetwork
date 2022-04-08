import datetime
import os
import re
import json
import logging

from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage

from authorization.models import UserFile
from createPosts.models import Posts
from .news import DataNewsCreator
from services.forms import CoverForm
from .models import UserSession

module_logger = logging.getLogger(name='ex.user')


def user_template(request, user_id):
    try:
        user = User.objects.get(id=user_id)
    except Exception as ex:
        module_logger.exception(ex)
        return redirect('/')

    post = None

    try:
        post = Posts.objects.filter(user_id=user_id).order_by('-user_date')
    except Posts.DoesNotExist:
        module_logger.exception(Posts.DoesNotExist)

    try:
        if request.session['sessionID'] and request.session['sessionID'] == int(user_id):
            name = f'{user.first_name} {user.last_name}'
            date = datetime.datetime.now().date()
            data_news_creator = DataNewsCreator()
            news_data = data_news_creator.create_news_data()

            cover_form = CoverForm(request.POST, request.FILES)
            cover_photo = UserFile.objects.get(id=user_id).cover_photo

            UserSession.id = user_id
            UserSession.fullname = name
            UserSession.login = user.username
            UserSession.cover_photo = cover_photo

            try:
                re.findall(r'\w', cover_photo.name)
            except Exception as ex:
                module_logger.exception(ex)
                cover_photo = " "

            if len(str(cover_photo).strip()) == 0:
                cover_photo = " "

            data_dict = {**UserSession.data_dict,
                         **{'name': name, 'user_id': user_id, 'user_post_dict': post, 'date': date,
                            'news_data': news_data, 'cover_photo': cover_photo, 'cover_form': cover_form}}
            return render(request, 'user.html', data_dict)
        else:
            return redirect('/')
    except Exception as ex:
        module_logger.exception(ex)
        return redirect(to='/')


def logout_user(request):
    logout(request)
    return redirect(to='/')


def change_cover(request):
    if request.method == 'POST':
        user_id = int(request.session['sessionID'])
        user = UserFile.objects.get(id=user_id)

        try:
            os.remove(path=f'{os.getcwd()}\\{user.cover_photo}')
        except Exception as ex:
            module_logger.exception(ex)

        try:
            file = request.FILES
            fs = FileSystemStorage()
            file_name = fs.save(file['cover_photo'].name, file['cover_photo'])
            upload_file_url = fs.url(file_name)
            UserFile.objects.filter(id=user_id).update(cover_photo=upload_file_url)
        except Exception as ex:
            module_logger.exception(ex)

    return HttpResponse('Изображение получено!')


def search_friends(request):
    try:
        result = json.loads(request.body)
        user_id = request.session['sessionID']
        friends_name = [(x.user_name.strip(), x.id, x.avatar.name.strip()) for x in UserFile.objects.all() if
                        x.user_name.strip().lower().startswith(result['friendsSearch']) and x.id != user_id]
    except Exception as ex:
        module_logger.exception(ex)

    return HttpResponse(json.dumps(friends_name))
