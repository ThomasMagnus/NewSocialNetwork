from django.db import models
from django.contrib.postgres.fields import ArrayField


class UserFile(models.Model):

    class Meta:
        db_table = 'userfile'
        verbose_name = 'пользователь'
        verbose_name_plural = 'Пользователи'

    id = models.IntegerField(primary_key=True)
    user_name = models.CharField(max_length=128)
    user_login = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    password = models.TextField()
    phone = models.CharField(max_length=14)
    avatar = models.ImageField(upload_to='media/avatar/%Y/%m/%d')
    is_staff = models.BooleanField()
    is_superuser = models.BooleanField()
    first_login = models.DateTimeField()
    last_join = models.TextField()
    dateJoin = models.DateTimeField()
    cover_photo = models.ImageField(upload_to='images/%Y/%m/%d')
    friend_mass = ArrayField(models.TextField())
    photo = ArrayField(models.TextField())
    community = ArrayField(models.TextField())

    def __str__(self):
        return f'{self.email}, {self.user_login}, {self.cover_photo}, {self.id}'


class ProFile(models.Model):

    class Meta:
        db_table = 'profile'
        verbose_name = 'данные пользователя'
        verbose_name_plural = 'данных пользователя'

    user_id = models.BigIntegerField(primary_key=True)
    user_login = models.CharField(max_length=50)
    city = models.TextField()
    education = models.TextField()
    university = models.TextField()
    sex = models.CharField(max_length=1)
    born_date = models.DateField()
    job = models.TextField()
    job_position = models.TextField()
    receipt_date = models.DateField()
    bio = models.TextField()
