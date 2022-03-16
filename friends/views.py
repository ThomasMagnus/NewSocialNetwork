from django.shortcuts import render
from users.models import UserData
from users.news import DataNewsCreator


def friend_template(request):

    data_new_creator = DataNewsCreator()
    news = data_new_creator.create_news_data()

    return render(request, 'friends_menu.html', {**UserData.data_dict, **{'name': UserData.name, 'cover_photo': UserData.cover_photo, 'news_data': news}})
