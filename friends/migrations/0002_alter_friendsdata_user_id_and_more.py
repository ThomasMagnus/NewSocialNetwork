# Generated by Django 4.0 on 2022-05-26 12:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('authorization', '__first__'),
        ('friends', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='friendsdata',
            name='user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='authorization.userfile'),
        ),
        migrations.AlterField(
            model_name='friendsrequest',
            name='user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='authorization.userfile'),
        ),
    ]