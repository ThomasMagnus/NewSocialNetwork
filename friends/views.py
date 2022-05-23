import json

from django.http import HttpResponse
from django.db.models import QuerySet
from django.shortcuts import render

from authorization.models import UserFile
from users.news import DataNewsCreator
from users.models import UserSession
from .models import Friends
from django.contrib.auth.models import User
from services.data_classes import FriendsData


def friend_template(request):
    data_new_creator = DataNewsCreator()
    news = data_new_creator.create_news_data()
    id: int = request.session['sessionID']
    user: User = User.objects.get(id=id)
    user_cover_photo: str = UserFile.objects.get(id=id).cover_photo
    username: str = f'{user.first_name} {user.last_name}'

    return render(request, 'friends_menu.html', {**UserSession.data_dict, **{'name': username,
                                                                             'cover_photo': user_cover_photo,
                                                                             'news_data': news}})


def sorted_friends(sort_list: QuerySet, sort_data: list):
    friends_data: FriendsData
    for item in sort_list:
        friends_data = FriendsData(name=item.friend_name, login=item.friend_login, email=item.friend_email,
                                   status=item.status, date=item.date.strftime("%d.%m.%Y"),
                                   request_on_friend=item.request_on_friend)
        sort_data.append(friends_data.parse_friends_data())


def get_friends_list(request):
    # id = request.session['sessionID']
    # user: User = User.objects.get(id=id)
    # login: str = user.username
    # Friends._meta.db_table = f'friends_{login}'
    # print(Friends._meta.db_table)
    friends: QuerySet = Friends.objects.filter(status=True)
    friends_requests: QuerySet = Friends.objects.filter(request_on_friend=True)
    friends_list: list = []
    friends_requests_list: list = []

    sorted_friends(friends, friends_list)
    sorted_friends(friends_requests, friends_requests_list)

    data = {
        'friendsData': friends_list,
        'friendsRequests': friends_requests_list
    }

    return HttpResponse(json.dumps(data))
