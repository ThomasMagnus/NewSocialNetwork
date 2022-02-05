from django.db import models


class News(models.Model):
    class Meta:
        db_table = 'News'
        verbose_name = 'новость'
        verbose_name_plural = 'Новости'

    title = models.TextField()
    news_link = models.TextField()