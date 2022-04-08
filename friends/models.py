from django.db import models
from users.models import UserSession


class Friends(models.Model):
    class Meta:
        db_table: str = f'friends_{UserSession.login}'

    friend_name = models.TextField()
    friend_login = models.TextField()
    friend_email = models.TextField()
    status = models.BooleanField()
    date = models.DateTimeField()
    request_on_friend = models.BooleanField()
