# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('musicdb', '0006_auto_20151205_2013'),
    ]

    operations = [
        migrations.AlterField(
            model_name='song',
            name='lyrics',
            field=models.TextField(null=True),
        ),
    ]
