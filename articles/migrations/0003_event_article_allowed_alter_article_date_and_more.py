# Generated by Django 4.0.5 on 2024-04-23 10:32

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0002_alter_article_date_alter_event_date_end_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='event_article',
            name='allowed',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='article',
            name='date',
            field=models.DateField(default=datetime.datetime(2024, 4, 23, 10, 32, 2, 397448, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='event',
            name='date_end',
            field=models.DateField(default=datetime.datetime(2024, 4, 23, 10, 32, 2, 394446, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='event',
            name='date_start',
            field=models.DateField(default=datetime.datetime(2024, 4, 23, 10, 32, 2, 394446, tzinfo=utc)),
        ),
    ]
