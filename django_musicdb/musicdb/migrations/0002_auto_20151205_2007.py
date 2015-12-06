# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('musicdb', '0001_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Publisher',
        ),
        migrations.RemoveField(
            model_name='album',
            name='artist_id',
        ),
        migrations.RemoveField(
            model_name='song',
            name='album_id',
        ),
    ]
