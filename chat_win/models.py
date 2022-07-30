from typing import Dict, Any

from django.db import models

from authorization.models import UserFile


class Chat(models.Model):
    class Meta:
        db_table = 'messages'
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'

    id = models.AutoField(primary_key=True)
    user_id_from = models.IntegerField(null=False)
    user_id_to = models.IntegerField(null=False)
    date_write_message = models.CharField(max_length=16)
    message_text = models.TextField(null=False)


class Messages(models.Model):
    class Meta:
        db_table = 'default_name'

    id = models.AutoField(primary_key=True)
    user_id = models.IntegerField()
    user_id_to = models.IntegerField()
    date_write = models.DateTimeField()
    message_text = models.TextField()


class MessagesTable(models.Model):
    class Meta:
        db_table = 'messages_data_table'

    id = models.IntegerField(primary_key=True)
    user = models.ForeignKey(UserFile, on_delete=models.CASCADE)
    table_name = models.TextField()
    creation_date = models.DateTimeField()


class UserMessages(models.Model):
    id = models.IntegerField(primary_key=True)
    user = models.ForeignKey(UserFile, on_delete=models.CASCADE)
    message_text = models.TextField()
    message_date = models.DateTimeField()


class ModelSet(object):
    def __init__(self, donor_record_name):
        self.donor_record_name = donor_record_name

    def _create_model(self, model_name: str = None, meta_opt: Dict[str, str] = None, base_model_class=models.Model,
                      fields=None) -> type:
        class Meta:
            app_label = 'chat_win'
            db_table = self.donor_record_name

        if meta_opt is not None:
            for key, value in meta_opt.items():
                setattr(Meta, key, value)

        set_attrs: Dict[str, Any] = {
            '__module__': self.__class__.__module__,
            'Meta': Meta,
            'objects': models.Manager()
        }

        if fields:
            set_attrs.update(fields)

        model = type(model_name, (base_model_class, ), set_attrs)

        return model

    def create_model(self):
        fields: Dict[str, Any] = {
            'id': models.IntegerField(primary_key=True),
            'user': models.ForeignKey(UserFile, on_delete=models.CASCADE),
            'message_text': models.TextField(),
            'message_date': models.DateTimeField(),
        }

        return self._create_model(model_name='UserMessages', fields=fields)
