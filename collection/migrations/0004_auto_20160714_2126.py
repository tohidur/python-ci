# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('collection', '0003_auto_20160713_1116'),
    ]

    operations = [
        migrations.AlterField(
            model_name='collection',
            name='privacy',
            field=models.NullBooleanField(default=True),
        ),
    ]
