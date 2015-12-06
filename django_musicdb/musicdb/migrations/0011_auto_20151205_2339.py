# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('musicdb', '0010_auto_20151205_2333'),
    ]

    operations = [
        migrations.AlterField(
            model_name='keyword',
            name='song',
            field=models.ForeignKey(related_name='keywords', default=1, to='musicdb.Song', null=True),
        ),
    ]
