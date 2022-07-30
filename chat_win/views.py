import datetime
import json
from typing import List, Dict, Any, Tuple
import logging

import requests
from django.db.models.base import ModelBase

from .models import Chat, Messages, MessagesTable, UserMessages, ModelSet
from authorization.models import UserFile
from users.models import UserSession
from users.news import DataNewsCreator
from registration.models import MessageTable

from django.shortcuts import render
from django.db.models import QuerySet
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

module_logger = logging.getLogger('ex.chat_win')


@csrf_exempt
def get_chats(request):
    if request.method == 'GET':
        user_id: int = int(request.session['sessionID'])
        chat: QuerySet = Messages.objects.filter(user_id=user_id).order_by('user_id_to', '-date_write').distinct(
            'user_id_to')
        data: List[Dict[str, str]] = [
            {'name': UserFile.objects.get(id=y.user_id_to).user_name.strip(), 'chat_id': y.user_id_to,
             'message_text': y.message_text, 'friend_avatar': str(UserFile.objects.get(id=y.user_id_to).avatar).strip()}
            for y in chat]
        return data


def chat_window(request):
    try:
        user_id = request.session['sessionID']
        user: UserFile = UserFile.objects.get(id=user_id)
        Messages._meta.db_table = f'{str(user.user_login).strip()}_toSendMessage'
        messages: QuerySet = Messages.objects.filter(user_id=user_id).order_by('user_id_to', '-date_write').distinct(
            'user_id_to')
        # for item in messages:
        #     print(item.message_text)
        news: List[Dict[str, str]] = DataNewsCreator().create_news_data()
        chats = get_chats(request)
        # chats = get_messages_data(request, False)
        data_user_id: QuerySet = Messages.objects.all().distinct('user_id_to')

        return render(request, 'chat_win.html', {**UserSession.data_dict, **{'name': user.user_name, 'news_data': news,
                                                                             'cover_photo': user.cover_photo,
                                                                             'avatar': user.avatar, 'chats': chats}})
    except Exception as ex:
        module_logger.exception(repr(ex))
        print(repr(ex))


def get_messages_tables(user_id: int) -> List[Tuple[str, str]]:
    messages_table: QuerySet = MessagesTable.objects.filter(user_id=user_id)
    tables = [(x.id, x.table_name) for x in messages_table]
    return tables


def get_messages_data(request, formatter=True):
    user_id = request.session['sessionID']
    messages_tables: List[Tuple[str, str]] = get_messages_tables(user_id)
    messages_data: List[Dict[str, str]] = []
    for x in range(len(messages_tables)):
        MessageTableTests: ModelBase = ModelSet(donor_record_name=messages_tables[x][1]).create_model()
        data_set_messages: QuerySet = MessageTableTests.objects.all().order_by('message_date')
        data_list: List[Dict[str, Any]] = []
        messages_data.append({
            'dialog': messages_tables[x][1],
            'chat_id': messages_tables[x][0],
            'messages': {}
        })
        try:
            for elem in data_set_messages:
                data_list.append({'username': str(elem.user.user_name).strip(),
                                  'message_date': datetime.datetime.strftime(elem.message_date,
                                                                             '%d.%m.%y %H:%M'),
                                  'friend_avatar': str(elem.user.avatar).strip(),
                                  'message_text': elem.message_text})
        except Exception as ex:
            print(repr(ex))
        messages_data[x]['messages']['data'] = data_list

    return HttpResponse(json.dumps(messages_data)) if formatter else messages_data
