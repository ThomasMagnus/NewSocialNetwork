from django.db import models

from authorization.models import UserFile


class Photo(models.Model):
    class Meta:
        db_table = 'photo'
        verbose_name = 'фото'
        verbose_name_plural = 'фото'

    id = models.AutoField(primary_key=True)
    user_id = models.IntegerField()
    path = models.ImageField()
    date_load = models.DateTimeField()

