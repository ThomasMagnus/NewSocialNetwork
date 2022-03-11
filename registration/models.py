from django.db import models


class FriendsRequests(models.Model):
    id = models.AutoField(primary_key=True)
    friend_name = models.TextField()
    friend_login = models.TextField()
    friend_email = models.TextField()
    status = models.BooleanField()
    date = models.DateTimeField()
    request_on_friend = models.BooleanField()

    class Meta:
        db_table = 'no_name'
