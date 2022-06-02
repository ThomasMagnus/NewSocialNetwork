from django.http import HttpResponse
from django.shortcuts import render
from authorization.models import UserFile, ProFile
from friends.models import FriendsData
from users.models import UserSession
from users.news import DataNewsCreator
from createPosts.models import Posts

import json
import logging


module_logger = logging.getLogger(name='ex.friends_page')


def detect_photo(photo_path):
    if len(str(photo_path).strip()) == 0:
        return " "
    else:
        return photo_path


def get_friend_page(request, user_id):
    user = UserFile.objects.get(id=request.session['sessionID'])
    data_news_creator = DataNewsCreator()
    news_data = data_news_creator.create_news_data()
    friend = UserFile.objects.get(id=user_id)
    avatar = user.avatar
    cover_photo = detect_photo(user.cover_photo)
    cover_friend_photo = detect_photo(friend.cover_photo)
    friend_avatar = detect_photo(friend.avatar)

    if len(str(cover_photo).strip()) == 0:
        cover_photo = ""

    return render(request, 'friends_page2.html',
                  {**UserSession.data_dict,
                   **{'name': user.user_name, 'friend_name': friend.user_name, 'news_data': news_data, 'id': user_id,
                      'cover_photo': cover_photo, 'avatar': avatar, 'cover_friend_photo': cover_friend_photo,
                      'friend_avatar': friend_avatar}})


def get_friend_data(request, user_id):
    user = UserFile.objects.get(id=user_id)
    profile = ProFile.objects.get(user_id=user_id)
    posts = [{'post': x.post, 'date': str(x.user_date.strftime("%d.%m.%Y"))} for x in
             Posts.objects.all().filter(user_id=user_id)]
    status = None

    try:
        friends = FriendsData.objects.get(friend_login=user.user_login)
        status = friends.status
    except Exception as ex:
        module_logger.exception(repr(ex))

    data = {
        'name': user.user_name.strip(),
        'last_login': user.last_join,
        'born_date': profile.born_date,
        'job': profile.job,
        'job_position': profile.job_position,
        'friends': user.friend_mass,
        'avatar': str(user.avatar).strip(),
        'photos': user.photo,
        'community': user.community,
        'posts': posts,
        'status': status
    }

    data_json = json.dumps(data)
    return HttpResponse(data_json)
