# Generated by Django 3.2.13 on 2022-07-04 10:25

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('bgame', '0005_auto_20220629_2040'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bgame',
            name='want_play',
            field=models.ManyToManyField(related_name='test', through='bgame.WantPlay', to=settings.AUTH_USER_MODEL),
        ),
    ]