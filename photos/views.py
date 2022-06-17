import json
import os
import datetime
from typing import Any

from django.core.files.storage import FileSystemStorage
from django.db.models import QuerySet
from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from authorization.models import UserFile
from .models import Photo
from users.models import UserSession
from users.news import DataNewsCreator
from services.forms import AvatarForm
from services.compressor import compress_image


def get_photos(request):
    user_id: int = int(request.session['sessionID'])
    user = UserFile.objects.get(id=user_id)
    photo: QuerySet = Photo.objects.filter(user_id=user_id).order_by('-date_load')
    news = DataNewsCreator().create_news_data()
    pagination: bool = False
    photos = [x for x in photo[0:6]]

    form: AvatarForm = AvatarForm(request.POST, request.FILES)

    if len(photo) > 6:
        pagination = True

    return render(request, 'photos_page.html',
                  {**UserSession.data_dict, 'name': user.user_name, 'news_data': news, 'cover_photo': user.cover_photo,
                   'photo': photos, 'pagination': pagination, 'form': form})


def get_all_photos(request):
    start: int = 0
    end: int = 6
    pagination: bool = True

    if request.method == 'POST':
        photoCount: int = int(request.POST['photoCount'])

        start += photoCount
        end += photoCount

        user_id: int = int(request.session['sessionID'])
        photo: QuerySet = Photo.objects.filter(user_id=user_id).order_by('-date_load')

        if end >= len(photo):
            end = len(photo)
            pagination = False

        print(start, end)

        all_photos = [str(x.path).strip() for x in photo[start:end]]
    return HttpResponse(json.dumps({'all_photos': all_photos, 'pagination': pagination}))


def add_photo(request):
    if request.method == 'POST':
        user_id: int = int(request.session['sessionID'])
        file: Any = request.FILES
        fs = FileSystemStorage(location=rf'{os.getcwd()}\media\photos')
        file_name = fs.save(file['file'].name, file['file'])
        compress_file_name: str = compress_image(rf'{os.getcwd()}\media\photos\{file_name}')
        upload_file_url = os.path.basename(compress_file_name)
        os.remove(path=rf'{os.getcwd()}\media\photos\{file_name}')
        photo: Photo = Photo(user_id=user_id, path='/media/photos/' + upload_file_url,
                             date_load=datetime.datetime.now())
        photo.save()

        return HttpResponse("Запрос получен")


@csrf_exempt
def remove_photo(request):
    print(json.loads(request.body).get('photoId'))
    photo_id: int = int(json.loads(request.body).get('photoId'))
    os.remove(path=rf'{os.getcwd()}/{Photo.objects.get(id=photo_id).path}')
    Photo.objects.filter(id=photo_id).delete()
    return HttpResponse("Good!")
