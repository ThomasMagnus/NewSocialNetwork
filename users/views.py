import datetime
import re
import json
import logging
import os

from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage

from authorization.models import UserFile
from createPosts.models import Posts
from friends.models import FriendsData
from .news import DataNewsCreator
from services.forms import CoverForm, AvatarForm
from .models import UserSession
from PIL import Image

module_logger = logging.getLogger(name='ex.user')


class ReturnUserData:
    def __init__(self, user_file: UserFile, name: str, cover_photo, friends_table_name: str, avatar: str, buffer: str):
        self.user_file = user_file
        self.name = name
        self.date = datetime.datetime.now().date()
        self.cover_photo = cover_photo
        self.friends_table_name = friends_table_name.strip()
        self.avatar = avatar
        self.buffer = buffer

    def query_friends_table(self) -> list:
        friends: list = list(FriendsData.objects.filter(user_login=self.user_file.user_login, status='friend'))
        return friends


def compress_image(image_name, new_size_ratio=0.9, quality=60, width=None, height=None, to_jpg=True) -> str:
    img = Image.open(image_name)

    if new_size_ratio < 1.0:
        img.resize((int(img.size[0] * new_size_ratio), int(img.size[1] * new_size_ratio)), Image.ANTIALIAS)
        print("[+] New Image shape:", img.size)
    elif width and height:
        img.resize((width, height), Image.ANTIALIAS)

    filename, ext = os.path.splitext(image_name)

    if to_jpg:
        new_filename: str = f'{filename}_compressed.jpg'
    else:
        new_filename: str = f'{filename}_compressed{ext}'

    try:
        img.save(new_filename, quality=quality, optimize=True)
    except:
        img = img.convert('RBG')
        img.save(new_filename, quality=quality, optimize=True)

    return new_filename


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
            print(len(str(UserFile.objects.get(id=user_id).cover_photo).strip()))
            return_user_data: ReturnUserData = ReturnUserData(name=f'{user.first_name} {user.last_name}',
                                                              user_file=UserFile.objects.get(id=user_id),
                                                              cover_photo=UserFile.objects.get(id=user_id).cover_photo,
                                                              friends_table_name=f'friends_friends',
                                                              avatar=UserFile.objects.get(
                                                                  id=user_id).avatar.name.strip(),
                                                              buffer=UserFile.objects.get(
                                                                  id=user_id).buffer_zone.name)
            return_user_data.query_friends_table()
            news_data = DataNewsCreator().create_news_data()
            cover_form = CoverForm(request.POST, request.FILES)
            avatar_form = AvatarForm(request.POST, request.FILES)

            try:
                re.findall(r'\w', return_user_data.cover_photo.name)

                if len(str(return_user_data.cover_photo).strip()) == 0:
                    return_user_data.cover_photo = " "
            except Exception as ex:
                module_logger.exception(ex)
                return_user_data.cover_photo = " "

            data_dict = {**UserSession.data_dict,
                         **{'name': return_user_data.name, 'user_id': user_id, 'user_post_dict': post,
                            'date': return_user_data.date,
                            'news_data': news_data, 'cover_photo': return_user_data.cover_photo,
                            'cover_form': cover_form, 'avatar_form': avatar_form,
                            'friends': return_user_data.query_friends_table(),
                            'avatar': return_user_data.avatar}}

            return render(request, 'user.html', data_dict)
        else:
            return redirect('/')
    except Exception as ex:
        print(repr(ex))
        module_logger.exception(ex)


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
            fs = FileSystemStorage(location=rf'{os.getcwd()}\media\images')
            file_name = fs.save(file['cover_photo'].name, file['cover_photo'])
            new_file_name: str = compress_image(
                os.getcwd() + rf'\media\images\{file_name}')
            upload_file_url = os.path.basename(new_file_name)
            UserFile.objects.filter(id=user_id).update(cover_photo='/media/images/' + upload_file_url)
            os.remove(path=f'{os.getcwd()}\\media\images\{file_name}')
        except Exception as ex:
            module_logger.exception(ex)

    return HttpResponse('Изображение получено!')


def search_friends(request):
    try:
        result = json.loads(request.body)
        user_id = request.session['sessionID']
        friends_data = [(x.user_name.strip(), x.id, x.avatar.name.strip()) for x in UserFile.objects.all() if
                        x.user_name.strip().lower().startswith(result['friendsSearch']) and x.id != user_id]
    except Exception as ex:
        module_logger.exception(ex)

    return HttpResponse(json.dumps(friends_data))


def change_avatar(request):
    if request.method == 'POST':
        user_id = int(request.session['sessionID'])
        user = UserFile.objects.get(id=user_id)

        file_name = avatar(request, rf'{os.getcwd()}\media\avatar', f'{os.getcwd()}{user.avatar}')
        UserFile.objects.filter(id=user_id).update(avatar='/media/avatar/' + file_name)

    return HttpResponse('Файл получен сервером')


def buffer_zone(request):
    if request.method == 'POST':
        user_id = int(request.session['sessionID'])
        user = UserFile.objects.get(id=user_id)

        file_name = avatar(request, rf'{os.getcwd()}\media\avatar\buffer', f'{os.getcwd()}{user.buffer_zone}')

        UserFile.objects.filter(id=user_id).update(buffer_zone='/media/avatar/buffer/' + file_name)

        return HttpResponse('/media/avatar/buffer/' + file_name)


def avatar(request, path: str, path_del: str):
    try:
        os.remove(path_del)
    except Exception as ex:
        module_logger.exception(repr(ex))

    try:
        file = request.FILES
        fs = FileSystemStorage(location=path)
        file_name = fs.save(file['file'].name, file['file'])
        return  file_name
    except Exception as ex:
        module_logger.exception(repr(ex))


def del_buffer(request):
    user_id = int(request.session['sessionID'])
    user = UserFile.objects.get(id=user_id)

    os.remove(f'{os.getcwd()}{user.buffer_zone}')
    UserFile.objects.filter(id=user_id).update(buffer_zone='')
    return HttpResponse('Ok')
