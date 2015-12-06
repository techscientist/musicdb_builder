# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('musicdb', '0009_keyword'),
    ]

    operations = [
        migrations.AlterField(
            model_name='album',
            name='artist',
            field=models.ForeignKey(related_name='albums', default=1, to='musicdb.Artist', null=True),
        ),
        migrations.AlterField(
            model_name='song',
            name='album',
            field=models.ForeignKey(related_name='songs', default=1, to='musicdb.Album', null=True),
        ),
    ]
