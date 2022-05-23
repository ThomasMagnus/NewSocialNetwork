from django.db import models

from authorization.models import UserFile


class Friends(models.Model):
    class Meta:
        db_table: str = ''

    friend_name = models.CharField(max_length=120)
    friend_login = models.CharField(max_length=120)
    friend_email = models.CharField(max_length=50)
    status = models.BooleanField()
    date = models.DateTimeField()
    request_on_friend = models.BooleanField()
    friend_id = models.IntegerField()
