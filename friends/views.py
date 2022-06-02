import json
import logging

from django.http import HttpResponse
from django.db.models import QuerySet
from django.shortcuts import render

from authorization.models import UserFile
from users.news import DataNewsCreator
from users.models import UserSession
from .models import FriendsData, FriendsRequest
from django.contrib.auth.models import User
from services.data_classes import FriendsDataDict

module_logger = logging.getLogger(name='ex.friends')


def friend_template(request):
    data_new_creator = DataNewsCreator()
    news = data_new_creator.create_news_data()
    id: int = request.session['sessionID']
    user: User = User.objects.get(id=id)
    user_cover_photo: str = UserFile.objects.get(id=id).cover_photo
    username: str = f'{user.first_name} {user.last_name}'

    if len(str(user_cover_photo).strip()) == 0:
        user_cover_photo = " "

    return render(request, 'friends_menu.html', {**UserSession.data_dict, **{'name': username,
                                                                             'cover_photo': user_cover_photo,
                                                                             'news_data': news}})


def sorted_friends(sort_list: QuerySet, sort_data: list):
    friends_data: FriendsDataDict
    for item in sort_list:
        friends_data = FriendsDataDict(firstname=item.friend_firstname, lastname=item.friend_lastname, login=item.friend_login)
        sort_data.append(friends_data.parse_friends_data())


def get_friends_list(request):
    print(request.session.items())
    try:
        id = request.session['sessionID']
        user: User = User.objects.get(id=id)
        # login: str = user.username
        # Friends._meta.db_table = f'friends_{login}'
        friends: QuerySet = FriendsData.objects.filter(user_login=user.username, status='friend')
        friends_requests: QuerySet = FriendsData.objects.filter(user_login=user.username, status='request')
        friends_list: list = []
        friends_requests_list: list = []

        sorted_friends(friends, friends_list)
        sorted_friends(friends_requests, friends_requests_list)

        data = {
            'friendsData': friends_list,
            'friendsRequests': friends_requests_list
        }

        return HttpResponse(json.dumps(data))
    except Exception as ex:
        module_logger.exception(ex)
        print(repr(ex))
        return HttpResponse(repr(ex))
