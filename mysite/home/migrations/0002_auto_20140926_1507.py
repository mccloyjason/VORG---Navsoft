# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user_details',
            name='date',
            field=models.DateField(default=datetime.date(2014, 9, 26)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user_details',
            name='status',
            field=models.CharField(max_length=200, default=datetime.date(2014, 9, 26)),
            preserve_default=False,
        ),
    ]
