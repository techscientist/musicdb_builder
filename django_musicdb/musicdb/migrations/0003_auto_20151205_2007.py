# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('musicdb', '0002_auto_20151205_2007'),
    ]

    operations = [
        migrations.AlterField(
            model_name='album',
            name='year',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='artist',
            name='rank',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='song',
            name='year_released',
            field=models.IntegerField(),
        ),
    ]
