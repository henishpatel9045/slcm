# Generated by Django 3.2.7 on 2022-10-07 09:29

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('entities', '0002_auto_20221007_1449'),
    ]

    operations = [
        migrations.AlterField(
            model_name='school',
            name='highest_standard',
            field=models.IntegerField(default=12, validators=[django.core.validators.MinValueValidator(1, "Can't have standard lower than 1."), django.core.validators.MaxValueValidator(12, "Can't have standard higher than 12.")]),
        ),
    ]