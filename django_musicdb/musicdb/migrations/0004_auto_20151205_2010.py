# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('musicdb', '0003_auto_20151205_2007'),
    ]

    operations = [
        migrations.AddField(
            model_name='album',
            name='artist',
            field=models.ForeignKey(default=1, to='musicdb.Artist', null=True),
        ),
        migrations.AddField(
            model_name='song',
            name='album',
            field=models.ForeignKey(default=1, to='musicdb.Album', null=True),
        ),
    ]
