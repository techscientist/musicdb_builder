# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('musicdb', '0007_auto_20151205_2016'),
    ]

    operations = [
        migrations.AlterField(
            model_name='song',
            name='status',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
