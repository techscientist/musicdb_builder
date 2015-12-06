# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('musicdb', '0008_auto_20151205_2016'),
    ]

    operations = [
        migrations.CreateModel(
            name='Keyword',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('term', models.CharField(max_length=255)),
                ('appearances', models.IntegerField()),
                ('song', models.ForeignKey(default=1, to='musicdb.Song', null=True)),
            ],
        ),
    ]
