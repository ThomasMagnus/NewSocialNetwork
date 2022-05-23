from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from authorization.models import UserFile, ProFile
from friends.models import Friends
from users.models import UserSession
from users.news import DataNewsCreator
from createPosts.models import Posts

import json


def get_friend_page(request, user_id):
    user = UserFile.objects.get(id=request.session['sessionID'])
    data_news_creator = DataNewsCreator()
    news_data = data_news_creator.create_news_data()
    cover_photo = user.cover_photo
    friend = UserFile.objects.get(id=user_id)
    return render(request, 'friends_page2.html',
                  {**UserSession.data_dict,
                   **{'name': user.user_name, 'friend_name': friend.user_name, 'news_data': news_data, 'id': user_id, 'cover_photo': cover_photo}})


def get_friend_data(request, user_id):
    user = UserFile.objects.get(id=user_id)
    profile = ProFile.objects.get(user_id=user_id)
    posts = [{'post': x.post, 'date': str(x.user_date.strftime("%d.%m.%Y"))} for x in
             Posts.objects.all().filter(user_id=user_id)]

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
        'posts': posts
    }

    data_json = json.dumps(data)
    return HttpResponse(data_json)
