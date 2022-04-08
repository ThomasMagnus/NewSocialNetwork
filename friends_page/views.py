from django.shortcuts import render
from authorization.models import UserFile
from users.models import UserSession
from users.news import DataNewsCreator


def get_friend_page(request, user_id):
    user = UserFile.objects.get(id=user_id)
    data_news_creator = DataNewsCreator()
    news_data = data_news_creator.create_news_data()

    return render(request, 'friend_page.html', {**UserSession.data_dict, **{'name': user.user_name, 'news_data': news_data}})
