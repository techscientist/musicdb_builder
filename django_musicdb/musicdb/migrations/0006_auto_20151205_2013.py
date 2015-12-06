# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('musicdb', '0005_remove_song_year_released'),
    ]

    operations = [
        migrations.AlterField(
            model_name='song',
            name='keyword_dict',
            field=models.TextField(null=True),
        ),
    ]
