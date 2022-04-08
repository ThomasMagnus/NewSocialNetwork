import json

from django.http import HttpResponse
from django.db.models import QuerySet
from django.shortcuts import render
from users.news import DataNewsCreator
from users.models import UserSession
from .models import Friends


class FriendsData:
    def __init__(self, name: str, email: str, login: str, status: bool, date: str, request_on_friend: bool):
        self.name = name
        self.email = email
        self.login = login
        self.status = status
        self.date = date
        self.request_on_friend = request_on_friend

    def parse_friends_data(self) -> dict:
        data_object: dict = {
            'name': self.name,
            'email': self.email,
            'login': self.login,
            'status': self.status,
            'date': self.date,
            'request_on_friend': self.request_on_friend
        }

        return data_object


def friend_template(request):
    data_new_creator = DataNewsCreator()
    news = data_new_creator.create_news_data()

    return render(request, 'friends_menu2.html', {**UserSession.data_dict, **{'name': UserSession.fullname,
                                                                              'cover_photo': UserSession.cover_photo,
                                                                              'news_data': news}})


def sorted_friends(sort_list: QuerySet, sort_data: list):
    friends_data: FriendsData
    for item in sort_list:
        friends_data = FriendsData(name=item.friend_name, login=item.friend_login, email=item.friend_email,
                                   status=item.status, date=item.date.strftime("%d.%m.%Y"), request_on_friend=item.request_on_friend)
        sort_data.append(friends_data.parse_friends_data())


def get_friends_list(request):

    Friends._meta.db_table = f'friends_{UserSession.login}'
    friends: QuerySet = Friends.objects.filter(status=True)
    friends_requests: QuerySet = Friends.objects.filter(request_on_friend=True)
    friends_list: list = []
    friends_requests_list: list = []

    sorted_friends(friends, friends_list)
    sorted_friends(friends_requests, friends_requests_list)
    print(friends_requests_list)

    data = {
        'friendsData': friends_list,
        'friendsRequests': friends_requests_list
    }

    return HttpResponse(json.dumps(data))
