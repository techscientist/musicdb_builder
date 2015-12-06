# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('musicdb', '0004_auto_20151205_2010'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='song',
            name='year_released',
        ),
    ]
