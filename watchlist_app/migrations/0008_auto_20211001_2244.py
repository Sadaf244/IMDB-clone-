# Generated by Django 3.2.6 on 2021-10-01 17:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('watchlist_app', '0007_auto_20211001_2224'),
    ]

    operations = [
        migrations.AddField(
            model_name='watchlist',
            name='avg_rating',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='watchlist',
            name='number_rating',
            field=models.IntegerField(default=0),
        ),
    ]
