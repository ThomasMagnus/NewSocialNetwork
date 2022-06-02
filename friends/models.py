from django.db import models

from authorization.models import UserFile


class FriendsData(models.Model):
    class Meta:
        db_table = 'friends_data'

    id = models.AutoField(primary_key=True)
    # user_id = models.ForeignKey(UserFile, on_delete=models.PROTECT)
    firstname = models.CharField(max_length=150)
    lastname = models.CharField(max_length=150)
    user_login = models.CharField(max_length=150)
    friend_id = models.IntegerField()
    friend_firstname = models.CharField(max_length=150)
    friend_lastname = models.CharField(max_length=150)
    friend_login = models.CharField(max_length=150)
    status = models.TextField(default='')
    request_date = models.DateTimeField(default='')


class FriendsRequest(models.Model):
    class Meta:
        db_table = 'friends_request'

    id = models.AutoField(primary_key=True)
    # user_id = models.ForeignKey(UserFile, on_delete=models.PROTECT)
    firstname = models.CharField(max_length=150)
    lastname = models.CharField(max_length=150)
    user_login = models.CharField(max_length=150)
    friend_id = models.IntegerField()
    friend_firstname = models.CharField(max_length=150)
    friend_lastname = models.CharField(max_length=150)
    friend_login = models.CharField(max_length=150)